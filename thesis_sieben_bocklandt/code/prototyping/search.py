import tqdm
from abc import ABC, abstractmethod
from math import comb, prod
from copy import copy, deepcopy
from heapq import heappush, heappop
from typing import Any, Dict, Set, Tuple, List, Iterable, FrozenSet, Callable
from argparse import ArgumentParser
from collections import defaultdict
from functools import lru_cache
from itertools import product, combinations


Slide = FrozenSet["Predicate"]
Move = Set[Tuple["Predicate", "Predicate"]]
Substitution = Dict[int, int]
Similarity = Callable[[Slide, Slide], Tuple[float, Substitution]]


class Predicate:
    """Generic predicate."""

    def __init__(self, name: str, *args):
        self.name = name
        self.arguments = tuple(args)

    def __eq__(self, other: "Predicate"):
        return self.name == other.name and self.arguments == other.arguments

    def __hash__(self):
        return hash((self.name, self.arguments))

    def __getitem__(self, i: int):
        assert i < len(self.arguments)
        return self.arguments[i]

    def __str__(self):
        return "{}({})".format(self.name, ",".join(map(str, self.arguments)))

    def __repr__(self):
        return str(self)

    def apply(self, s: Substitution) -> "Predicate":
        return Predicate(self.name, *[s[a] if a in s else a for a in self.arguments])

    def reverse(self) -> "Predicate":
        return Predicate(self.name, *[-a for a in self.arguments])

    @property
    def arity(self):
        return len(self.arguments)

    @classmethod
    def from_string(self, string: str):
        pass

    @classmethod
    def from_string_sieben(self, string: str):
        if "+" not in string:
            return Predicate(string)
        name, arguments = string.split("+")
        arguments = [int(a) for a in arguments.split("_")]
        return Predicate(name, *arguments)


class Searcher(ABC):
    """Base searcher class."""

    def __init__(
        self,
        predicates: List[List[str]],
        similarity: Similarity = None,
        max_depth: int = 2,
    ):
        """

        Args:
            predicates: List of lists of interchangable predicates.

        """
        self.pmap = {p: set(l) - {p} for l in predicates for p in l}
        self.similarity = similarity or similarity_optimal
        self.max_depth = max_depth

    @abstractmethod
    def search(
        self,
        slide: Set[Predicate],
        archetypes: List[Set[Predicate]],
    ):
        pass

    def replacements(self, p: Predicate) -> List[Predicate]:
        """Get possible replacements for predicate."""
        if p.name in self.pmap:
            return [Predicate(n, *p.arguments) for n in self.pmap[p.name]]
        return [p]


class BreadthSearcher(Searcher):
    """Breadth first in terms of number of replaced objects."""

    def __init__(
        self,
        predicates: List[List[str]],
        similarity: Similarity = None,
        max_depth: int = 2,
        beam: int = 0,
    ):
        """

        Args:
            beam: Beam width. If not set, defaults to
                not using a beam.

        """
        super().__init__(predicates, similarity, max_depth)
        self.beam = beam

    def search(
        self,
        slide: Set[Predicate],
        archetypes: List[Set[Predicate]],
    ):
        """Search for archetype.

        Returns:
            List of (i, moves, score) tuples with i an
            index in archetypes.

        """
        slide = frozenset(slide)
        conditions = set()
        for depth in range(self.max_depth + 1):
            scores = list()
            moves = self.expansions(slide, depth, conditions)
            for move in tqdm.tqdm(moves, desc="depth {}".format(depth)):
                new_slide = apply(slide, move)
                score, matches = best_matches(new_slide, archetypes, self.similarity)
                heappush(scores, (-score, move, matches))
            # perfect solution, stop
            if scores[0][0] == -1:
                break
            # apply beam, get best scores
            if self.beam > 0:
                conditions = set()
                bestscores = set()
                while len(scores) > 0 and len(bestscores) < self.beam:
                    d, move, _ = heappop(scores)
                    bestscores.add(d)
                    conditions.add(move)
        # get top scores
        return [s for s in scores if s[0] == min(s for s, _, _ in scores)]

    def expansions(
        self,
        slide: Set[Predicate],
        moves: int,
        conditions: Set[Move] = None,
    ) -> List[Move]:
        """Expand a slide.

        Args:
            moves: Number of moves.
            conditions: A set of conditions. Each condition
                is a set of moves.

        Returns:
            A list of expansions, where each expansion
            is a set of tuples (x, y) that indicate
            predicate x has to be replace by y.

        """
        if conditions is None:
            conditions = set()
        # list of predicates to try replacing
        to_replace = {p for p in slide if p.name in self.pmap}
        # generate combinations of elements to move
        expansions = set()
        for combination in combinations(to_replace, moves):
            replacements = [self.replacements(p) for p in combination]
            for replacement in product(*replacements):
                candidate = frozenset(
                    (combination[i], p) for i, p in enumerate(replacement)
                )
                if len(conditions) == 0 or any(
                    condition.issubset(candidate) for condition in conditions
                ):
                    expansions.add(candidate)
        return expansions

    def __str__(self) -> str:
        return "BreadthSearcher(max_depth={},similarity={},beam={})".format(
            self.max_depth, self.similarity.__name__, self.beam
        )


class GreedySearcher(Searcher):
    """Greedy search."""

    def search(
        self,
        slide: Slide,
        archetypes: List[Slide],
    ):
        n_moves = 0
        m_moves = self.max_moves(slide)
        # all possible moves used during search
        all_moves = self.moves(slide)
        # initalise heap with (score, indices, moves) where
        # indices are indices into the list of archetypes
        heap = [(*best_matches(slide, archetypes, self.similarity), set())]
        while n_moves < m_moves:
            score, matches, moves = heappop(heap)
            # perfect score, add back to heap and break
            # from search
            if score == -1:
                heappush(heap, (score, matches, moves))
                break
            # get moves of objects that were not moved before
            # by checking arguments
            moved = {move[0].arguments for move in moves}
            moves_left = {move for move in all_moves if move[0].arguments not in moved}
            # apply move and add to queue
            for move in tqdm.tqdm(moves_left, desc="{}/{}".format(n_moves, m_moves)):
                new_move = moves | {move}
                new_slide = apply(slide, new_move)
                new_score, new_matches = best_matches(
                    new_slide, archetypes, self.similarity
                )
                heappush(heap, (-new_score, new_matches, new_move))
            # count number of moves
            n_moves += len(moves_left)
        # extract results by popping best from heap
        results = [heappop(heap)]
        while True:
            result = heappop(heap)
            if result[0] == results[0][0]:
                results.append(result)
            else:
                break
        return results

    def moves(self, slide: Slide) -> List[Tuple[Predicate, Predicate]]:
        """List of moves for a slide."""
        expansions = list()
        for predicate in slide:
            for replacement in self.replacements(predicate):
                expansions.append((predicate, replacement))
        return expansions

    def max_moves(self, slide: Slide) -> int:
        """Compute number of elements."""
        N = [len(self.pmap[p.name]) for p in slide if p.name in self.pmap]
        C = combinations(N, self.max_depth)
        return sum(prod(c) for c in C)

    def __str__(self) -> str:
        return "GreedySearcher(max_depth={},similarity={})".format(
            self.max_depth, self.similarity.__name__
        )


def apply(slide: Slide, move: Move) -> Slide:
    """Aply move to slide."""
    new_slide = set(slide)
    for x, y in move:
        new_slide.discard(x)
        new_slide.add(y)
    return frozenset(new_slide)


def best_matches(slide: Slide, archetypes: List[Slide], similarity: Similarity):
    """Get best score of slide in archetypes.

    Returns:
        A tuple of `(score, indices)` with `indices` a list
        of all archetypes for which `score` is obtained.

    """
    best_archetypes = list()
    best_score = 0
    for i, archetype in enumerate(archetypes):
        d, _ = similarity(slide, archetype)
        if d == best_score:
            best_archetypes.append(i)
        elif d > best_score:
            best_archetypes = [i]
            best_score = d
    return (best_score, best_archetypes)


def similarity_approximate(S1: Slide, S2: Slide) -> Tuple[float, Substitution]:
    """Approximate similarity between slides.

    Returns:
        Similarity and empty substitution.

    """
    S1n = {p.name for p in S1}
    S2n = {p.name for p in S2}
    return jaccard(S1n, S2n), {}


def similarity_optimal(S1: Slide, S2: Slide) -> Tuple[float, Substitution]:
    """Compute similarity after optimal substitution.

    Returns:
        Jaccard similarity of sets after finding
        best substitution and mapping and used
        substitution.

    """
    # reverse
    S2 = {p.reverse() for p in S2}
    mappings = generate_functions(S1, S2)
    best_similarity = 0
    best_mapping = None
    for mapping in mappings:
        S1m = {p.apply(mapping) for p in S1}
        sim = jaccard(S1m, S2)
        if sim == 1:
            return 1, mapping
        elif sim >= best_similarity:
            best_similarity = sim
            best_mapping = mapping
    return best_similarity, best_mapping


def jaccard(S1: Set[Any], S2: Set[Any]):
    """Jaccard similarity between sets."""
    if len(S1) == 0 and len(S2) == 0:
        return 0
    i = len(S1 & S2)
    return i / (len(S1) + len(S2) - i)


def generate_functions(S1, S2):
    # generate initial and prune
    possibilities = generate_mappings(S1, S2)
    pruned = prune_mappings(possibilities)
    # generate combinations of remaining possible mappigns
    solutions = decide_mappings(pruned)
    # turn them into functional mappings
    mappings = list()
    for solution in solutions:
        mappings.extend(functional_mappings(solution))
    return mappings


def generate_mappings(
    S1: Iterable[Predicate], S2: Iterable[Predicate]
) -> Dict[int, Set[int]]:
    """Generate all possible mappings.

    Returns:
        A dictionary mapping each argument from S1
        to possible substitutions in S2.

    """
    possibilities = defaultdict(set)
    for p1 in S1:
        for p2 in S2:
            if p1.name == p2.name:
                for i, a in enumerate(p1.arguments):
                    possibilities[a].add(p2[i])
    return possibilities


def prune_mappings(
    S: Dict[int, Set[int]], to_check: Set[int] = None
) -> Dict[int, Set[int]]:
    """Remove trivial substitutions.

    Args:
        to_check: List of indices to start from. If not
            given, check all.

    Returns:
        Dictionary with trivial decisions propagated.

    """
    if to_check is None:
        to_check = S.keys()
    while len(to_check):
        to_remove = set()
        for k in to_check:
            if len(S[k]) == 1:
                element = next(iter(S[k]))
                to_remove.add((k, element))
        to_check = set()
        for k, e in to_remove:
            for i, values in S.items():
                if k != i:
                    try:
                        values.remove(e)
                        to_check.append(i)
                    except:
                        pass
    return {k: vs for k, vs in S.items() if len(vs) > 0}


def decide_mappings(S: Dict[int, Set[int]]) -> List[Dict[int, Set[int]]]:
    """Recursively make decisions and prune.

    Returns:
        A list mappings in which each value has length 1.

    """
    # found a solution
    if all(len(v) == 1 for v in S.values()):
        return [S]
    # pick smallest node to make decision for
    _, node = min((len(v), e) for e, v in S.items() if len(v) > 1)
    # recursively prune for all decisions
    solutions = list()
    for v in S[node]:
        # generate new dictionary
        Sn = deepcopy(S)
        Sn[node] = {v}
        # prune
        Sn = prune_mappings(Sn)
        # go to next level
        solutions.extend(decide_mappings(Sn))
    return solutions


def functional_mappings(S: Dict[int, Set[int]]) -> List[Substitution]:
    """Turn mapping into functional mappings.

    Returns:
        A list of functional mappings.

    """
    reverse = defaultdict(set)
    for k, vs in S.items():
        for v in vs:
            reverse[v].add(k)
    # decide on order of keys and possible values
    keys = sorted(reverse)
    values = [reverse[k] for k in keys]
    # turn combinations back into mappings
    return [{v: keys[i] for i, v in enumerate(c)} for c in product(*values)]


interchangable = [
    ["b-x", "f-x", "m-x", "o-x", "s-x", "d-x", "eq-x"],
    ["b-y", "f-y", "m-y", "o-y", "s-y", "d-y", "eq-y"],
]


if __name__ == "__main__":

    import json

    with open("learned.json") as f:
        learned = json.load(f)

    archetypes = list()
    for i, v1 in learned.items():
        for j, v2 in v1.items():
            for archetype in v2:
                archetypes.append(
                    frozenset(Predicate.from_string_sieben(s) for s in archetype)
                )

    slide = frozenset(
        Predicate.from_string_sieben(s)
        for s in {
            "f-y+3_0",
            "f-y+1_0",
            "b-y+4_0",
            "b-x+2_4",
            "s-x+2_0",
            "b-y+4_3",
            "eq-y+2_4",
            "s-x+2_1",
            "b-y+2_3",
            "b-x+1_4",
            "s-x+3_4",
            "o-x+0_3",
            "s-x+1_0",
            "eq-y+1_3",
            "b-y+2_1",
            "o-x+0_4",
            "b-y+4_1",
            "b-y+2_0",
            "b-x+1_3",
            "title+0",
            "f-x+2_3",
        }
    )

    searcher = BreadthSearcher(
        interchangable, max_depth=4, similarity=similarity_optimal, beam=2
    )
    # searcher = GreedySearcher(
    #     interchangable, max_depth=2, similarity=similarity_optimal
    # )
    print(searcher)
    print(searcher.search(slide, archetypes))