import itertools
from functools import lru_cache

from thesis_sieben_bocklandt.code.prototyping.classes import *
from thesis_sieben_bocklandt.code.prototyping.tree2RA import NOT_OVERLAPPING, OVERLAPPING
TITLE_SLIDE=({"title+0","first_slide"},1)
TITLE_SINGLE_CONTENT=({"title+0","middelboven+0","bi-y+0_1","overlapping-x+0_1"},2)
TITLE_DOUBLE_CONTENT=({"title+0","middelboven+0","bi-y+0_1","overlapping-x+0_1","bi-y+0_2","overlapping-y+1_2","not_overlapping-x+1_2"},3)
TITLE_TRIPLE_CONTENT=({"title+0","middelboven+0","bi-y+0_1","overlapping-x+0_1","bi-y+0_2","bi-y+0_3","overlapping-y+1_2","overlapping-y+1_3","overlapping-y+2_3","not_overlapping-x+1_2","not_overlapping-x+1_3","not_overlapping-x+2_3"},4)
COMPARISON=({"title+0","middelboven+0","bi-y+0_1","bi-y+0_2","bi-y+1_3","bi-y+2_4","overlapping-y+1_2","not_overlapping-x+1_2","overlapping-y+3_4","not_overlapping-x+3_4","overlapping-x+1_3","overlapping-x+2_4"},5)
SECTION_HEADER=({"title+0","middelmiddel+0"},1)
TITLE_ONLY=({"title+0","middelboven+0, no_content"},1)
CAPTIONED_CONTENT=({"bi-y+0_1","overlapping-x+0_1","not_overlapping-x+0_2","not_overlapping-x+1_2","overlapping-y+0_2","overlapping-y+1_2","no_title"},3)
BACKGROUND_QUOTE=({"title+0","middelmiddel+0","background+1"},2)
BACKGROUND_ONLY=({"background+0","no_title"},1)
ARCHETYPES=[TITLE_SLIDE,TITLE_SINGLE_CONTENT,TITLE_DOUBLE_CONTENT,TITLE_TRIPLE_CONTENT,COMPARISON,SECTION_HEADER,TITLE_ONLY,CAPTIONED_CONTENT,BACKGROUND_QUOTE,BACKGROUND_ONLY]
NAMES=["TITLE_SLIDE","TITLE_SINGLE_CONTENT","TITLE_DOUBLE_CONTENT","TITLE_TRIPLE_CONTENT","COMPARISON","SECTION_HEADER","TITLE_ONLY","CAPTIONED_CONTENT","BACKGROUND_QUOTE","BACKGROUND_ONLY"]

TITLE_SLIDE_RA=({"title+0","first_slide"},1)
TITLE_SINGLE_CONTENT_RA=({"title+0","middelboven+0","b-y+1_0","eq-x+0_1"},2)
TITLE_DOUBLE_CONTENT_RA=({"title+0","middelboven+0","b-y+1_0","s-x+1_0","f-x+2_0","b-y+2_0","eq-y+1_2","b-x+1_2"},3)
TITLE_TRIPLE_CONTENT_RA=({"title+0","middelboven+0","b-y+1_0","s-x+1_0","f-x+3_0","d-x+2_0","b-y+2_0","b-y+3_0","eq-y+1_2","eq-y+1_3","eq-y+2_3","b-x+1_2","b-x+1_3","b-x+2_3"},4)
COMPARISON_RA=({"title+0","middelboven+0","b-y+1_0","b-y+2_0","b-y+3_1","b-y+4_2","eq-y+1_2","b-x+1_2","eq-y+3_4","b-x+3_4","eq-x+1_3","eq-x+2_4","f-x+2_0","s-x+1_0"},5)
SECTION_HEADER_RA=({"title+0","middelmiddel+0"},1)
TITLE_ONLY_RA=({"title+0","middelboven+0, no_content"},1)
CAPTIONED_CONTENT_RA=({"b-y+1_0","eq-x+0_1","b-x+0_2","b-x+1_2","o-y+0_2","o-y+2_1","no_title"},3)
BACKGROUND_QUOTE_RA=({"title+0","middelmiddel+0","background+1"},2)
BACKGROUND_ONLY_RA=({"background+0","no_title"},1)
ARCHETYPES_RA=[TITLE_SLIDE_RA,TITLE_SINGLE_CONTENT_RA,TITLE_DOUBLE_CONTENT_RA,TITLE_TRIPLE_CONTENT_RA,COMPARISON_RA,SECTION_HEADER_RA,TITLE_ONLY_RA,CAPTIONED_CONTENT_RA,BACKGROUND_QUOTE_RA,BACKGROUND_ONLY_RA]

TITLE_SLIDE_LEARNED=([{'title+0', 'first_slide', 'b-y+1_0', 'd-x+1_0'}, {'title+0','first_slide', 'b-y+1_0', 'd-x+0_1'}, {'title+0','first_slide', 'b-y+1_0', 'd-x+1_0'}],2)
TITLE_SINGLE_CONTENT_LEARNED=([{'title+0', 'b-y+1_0', 's-x+1_0'}, {'s-x+0_1', 'title+0', 'b-y+1_0'}],2)
SECTION_HEADER_LEARNED=([{'title+0', 'b-y+1_0', 's-x+1_0'}, {'s-x+0_1', 'title+0', 'b-y+1_0'}],2)
TITLE_DOUBLE_CONTENT_LEARNED=([{'b-x+1_2', 'b-x+0_2', 'b-y+2_0', 's-x+1_0', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'s-x+0_1', 'b-x+1_2', 'b-x+0_2', 'b-y+2_0', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'b-x+1_2', 'b-y+2_0', 'b-x+0_2', 'd-y+1_2', 's-x+1_0', 'b-y+1_0', 'title+0'}, {'s-x+0_1', 'b-x+1_2', 'b-x+0_2', 'b-y+2_0', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'s-x+0_1', 'o-y+2_1', 'b-x+1_2', 'b-x+0_2', 'b-y+2_0', 'b-y+1_0', 'title+0'}, {'s-x+0_1', 'b-x+1_2', 'b-y+2_0', 'b-x+0_2', 'd-y+1_2', 'b-y+1_0', 'title+0'}, {'o-x+0_2', 'b-x+1_2', 'b-y+2_0', 's-x+1_0', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'o-x+0_2', 'b-x+1_2', 'b-y+2_0', 'd-y+1_2', 's-x+1_0', 'b-y+1_0', 'title+0'}, {'o-x+0_2', 'b-x+1_2', 'b-y+2_0', 's-x+1_0', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'o-y+2_1', 'o-x+0_2', 'b-x+1_2', 'b-y+2_0', 's-x+1_0', 'b-y+1_0', 'title+0'}]
,3)
TITLE_TRIPLE_CONTENT_LEARNED=([{'eq-y+1_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'b-x+0_2', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'eq-y+1_2', 'title+0', 'eq-y+2_3'}, {'d-y+3_2', 'eq-y+1_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_2', 'b-x+0_2', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'title+0'}, {'s-x+0_1', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+3_1', 'b-y+2_0', 'b-x+0_2', 'b-x+2_3', 'b-y+1_0', 'title+0', 'eq-y+2_3', 'd-y+2_1'}, {'d-y+2_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-x+0_2', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'd-y+1_3', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'s-x+0_1', 'd-y+3_2', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+3_1', 'b-x+0_2', 'b-y+2_0', 'b-x+2_3', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'d-y+2_3', 's-x+0_1', 'eq-y+1_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'b-x+0_2', 'b-x+2_3', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_2', 'b-x+0_2', 's-x+1_0', 'b-x+2_3', 'd-y+1_3', 'b-y+1_0', 'title+0', 'eq-y+2_3'}, {'s-x+0_1', 'eq-y+1_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'b-x+0_2', 'b-x+2_3', 'b-y+1_0', 'eq-y+1_2', 'title+0', 'eq-y+2_3'}, {'s-x+0_1', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_2', 'b-x+0_2', 'b-x+2_3', 'd-y+1_3', 'b-y+1_0', 'title+0', 'eq-y+2_3'}, {'d-y+2_3', 's-x+0_1', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-x+0_2', 'b-y+2_0', 'b-x+2_3', 'd-y+1_3', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'d-y+2_3', 's-x+0_1', 'b-y+3_0', 'o-y+1_2', 'b-x+0_3', 'b-x+1_2', 'b-x+1_3', 'b-y+2_0', 'b-x+0_2', 'd-y+1_3', 'b-y+1_0', 'b-x+3_2', 'title+0'}, {'s-x+0_1', 'd-y+3_2', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+3_1', 'b-x+0_2', 'b-y+2_0', 'b-x+2_3', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'d-y+2_3', 's-x+0_1', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+3_1', 'b-x+0_2', 'b-y+2_0', 'b-x+2_3', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'d-y+2_3', 's-x+0_1', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-x+0_2', 'b-y+2_0', 'b-x+2_3', 'd-y+1_3', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'d-y+2_3', 's-x+0_1', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-x+0_2', 'b-y+2_0', 'd-y+1_3', 'b-y+1_0', 'b-x+3_2', 'title+0', 'd-y+2_1'}, {'d-y+3_2', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_2', 'b-x+0_2', 's-x+1_0', 'b-x+2_3', 'd-y+1_3', 'b-y+1_0', 'title+0'}, {'d-y+2_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_2', 'b-x+0_2', 's-x+1_0', 'b-x+2_3', 'd-y+1_3', 'b-y+1_0', 'title+0'}, {'d-x+2_0', 'eq-y+1_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'eq-y+1_2', 'title+0', 'eq-y+2_3'}, {'d-y+3_2', 'eq-y+1_3', 'b-y+3_0', 'o-x+0_2', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+1_2', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'title+0'}, {'d-x+2_0', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+3_1', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'title+0', 'eq-y+2_3', 'd-y+2_1'}, {'d-x+2_0', 'd-y+2_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_3', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'d-x+2_0', 'o-x+0_3', 'd-y+2_3', 'b-y+3_0', 'b-x+1_2', 'b-x+1_3', 'b-y+2_0', 'd-y+1_3', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'d-y+3_2', 'b-y+3_0', 'o-x+0_2', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+3_1', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'d-x+2_0', 'd-y+2_3', 'eq-y+1_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'b-y+3_0', 'o-x+0_2', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_2', 's-x+1_0', 'b-x+2_3', 'd-y+1_3', 'b-y+1_0', 'title+0', 'eq-y+2_3'}, {'eq-y+1_3', 'b-y+3_0', 'o-x+0_2', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'eq-y+1_2', 'title+0', 'eq-y+2_3'}, {'d-y+2_3', 'eq-y+1_3', 'b-y+3_0', 'o-x+0_2', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'d-y+2_3', 'b-y+3_0', 'o-x+0_2', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_3', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'eq-y+1_2', 'title+0'}, {'d-y+2_3', 'o-x+0_3', 'b-y+3_0', 'o-y+1_2', 'b-x+1_2', 'b-x+1_3', 'b-y+2_0', 'b-x+0_2', 's-x+1_0', 'd-y+1_3', 'b-y+1_0', 'b-x+3_2', 'title+0'}, {'b-y+3_0', 'o-x+0_2', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+3_1', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'title+0', 'eq-y+2_3', 'd-y+2_1'}, {'d-y+3_2', 'b-y+3_0', 'o-x+0_2', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+3_1', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'d-x+2_0', 'd-y+2_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'd-y+3_1', 'b-y+2_0', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'d-x+2_0', 'd-y+2_3', 'b-y+3_0', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_3', 's-x+1_0', 'b-x+2_3', 'b-y+1_0', 'title+0', 'd-y+2_1'}, {'d-y+2_3', 'o-x+0_3', 'b-y+3_0', 'b-x+1_2', 'b-x+1_3', 'b-y+2_0', 'b-x+0_2', 's-x+1_0', 'd-y+1_3', 'b-y+1_0', 'b-x+3_2', 'title+0', 'd-y+2_1'}, {'d-y+2_3', 'o-x+0_3', 'b-y+3_0', 'b-x+1_2', 'b-x+1_3', 'b-y+2_0', 'd-y+1_2', 'b-x+0_2', 's-x+1_0', 'd-y+1_3', 'b-y+1_0', 'b-x+3_2', 'title+0'}, {'d-y+2_3', 'b-y+3_0', 'o-x+0_2', 'b-x+1_2', 'b-x+0_3', 'b-x+1_3', 'b-y+2_0', 'd-y+1_2', 's-x+1_0', 'b-x+2_3', 'd-y+1_3', 'b-y+1_0', 'title+0'}],4)
COMPARISON_LEARNED=([{'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'd-y+4_3', 'eq-y+1_2', 'b-y+3_2', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+0_3', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_3', 'b-x+0_3', 'b-x+2_3', 'b-x+1_4', 'b-y+2_3', 's-x+3_4', 'b-y+2_1', 'b-y+3_0', 's-x+1_2', 'b-y+4_3', 'b-x+0_4', 'eq-y+1_3', 'b-y+2_0', 's-x+1_0', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 'title+0', 'd-y+2_4', 's-x+2_0', 'b-x+2_4'}, {'b-x+1_3', 'b-x+0_3', 'b-x+2_3', 'b-x+1_4', 'b-y+2_3', 's-x+3_4', 'b-y+2_1', 'b-y+3_0', 's-x+1_2', 'b-y+4_3', 'b-x+0_4', 'eq-y+1_3', 's-x+0_2', 'b-y+2_0', 's-x+1_0', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 'title+0', 'd-y+2_4', 'b-x+2_4'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+0_3', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+4_2', 'b-x+1_2', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'd-y+4_3', 'eq-y+1_2', 'b-y+3_2', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+0_3', 's-x+4_2', 'b-x+1_2', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+0_3', 's-x+4_2', 'b-x+1_2', 'b-x+3_2', 'b-y+4_2'}, {'s-x+3_1', 'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 's-x+0_1', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 's-x+3_0', 'b-y+2_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 'b-x+0_2', 'title+0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'd-y+4_3', 'eq-y+1_2', 'b-y+3_2', 's-x+0_1', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 'b-y+2_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+0_3', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+2_1', 'b-x+2_4', 'b-y+3_2', 'b-y+3_0', 'b-y+3_1', 'b-y+1_2', 'title+2', 'b-x+3_1', 'b-x+0_4', 's-x+3_0', 'd-y+3_4', 'b-x+0_1', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'eq-y+0_1', 's-x+1_4', 's-x+3_2', 's-x+2_0', 'b-y+4_2', 'b-y+0_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 's-x+0_1', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 'd-y+3_4', 'b-y+2_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+0_3', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 's-x+0_1', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 'b-y+2_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+0_3', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'s-x+3_1', 'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 's-x+0_1', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 's-x+3_0', 'b-y+2_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 'b-x+0_2', 'title+0', 's-x+4_2', 'b-x+1_2', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'd-y+4_3', 'eq-y+1_2', 'b-y+3_2', 's-x+0_1', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 'b-y+2_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+0_3', 's-x+4_2', 'b-x+1_2', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 's-x+0_1', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 'b-x+0_4', 'b-y+2_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'b-x+0_2', 'title+0', 's-x+0_3', 's-x+4_2', 'b-x+1_2', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'o-x+0_4', 'title+0', 'd-x+2_0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'd-y+4_3', 'eq-y+1_2', 'b-y+3_2', 'b-y+3_0', 'b-y+3_1', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'o-x+0_4', 'title+0', 'd-x+2_0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'b-y+3_0', 'b-y+3_1', 's-x+3_0', 'd-y+3_4', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'o-x+0_4', 'title+0', 'd-x+2_0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'o-x+0_2', 'b-y+3_1', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'o-x+0_4', 'title+0', 's-x+4_2', 'b-x+1_2', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'd-y+4_3', 'eq-y+1_2', 'b-y+3_2', 'b-y+3_0', 'o-x+0_2', 'b-y+3_1', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'o-x+0_4', 'title+0', 's-x+4_2', 'b-x+1_2', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'b-y+3_0', 'o-x+0_2', 'b-y+3_1', 's-x+3_0', 'd-y+3_4', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'o-x+0_4', 'title+0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'd-y+4_3', 'eq-y+1_2', 'b-y+3_2', 'b-y+3_0', 'o-x+0_2', 'b-y+3_1', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'o-x+0_4', 'title+0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'o-x+0_2', 'b-y+3_1', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 's-x+1_3', 'o-x+0_4', 'title+0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'s-x+3_1', 'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'b-y+3_1', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 'o-x+0_4', 'title+0', 'd-x+2_0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'s-x+3_1', 'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'b-y+3_0', 'b-y+3_1', 's-x+3_0', 'd-y+3_4', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 'o-x+0_4', 'title+0', 'd-x+2_0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'s-x+3_1', 'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'o-x+0_2', 'b-y+3_1', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 'o-x+0_4', 'title+0', 's-x+4_2', 'b-x+1_2', 'b-x+3_2', 'b-y+4_2'}, {'s-x+3_1', 'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'b-y+3_0', 'o-x+0_2', 'b-y+3_1', 's-x+3_0', 'd-y+3_4', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 'o-x+0_4', 'title+0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}, {'s-x+3_1', 'b-x+1_4', 'eq-y+1_2', 'b-y+3_2', 'eq-y+3_4', 'b-y+3_0', 'o-x+0_2', 'b-y+3_1', 's-x+3_0', 'b-y+2_0', 's-x+1_0', 'b-x+3_4', 'b-y+4_1', 'b-y+4_0', 'b-y+1_0', 'o-x+0_4', 'title+0', 'b-x+1_2', 's-x+2_4', 'b-x+3_2', 'b-y+4_2'}],5)
TITLE_ONLY_LEARNED=([{'title+0', 'no_content'}],1)
CAPTIONED_CONTENT_LEARNED=([{'b-x+1_2', 'b-y+2_0', 'd-y+1_2', 'no_title', 's-x+1_0', 'b-y+1_0', 'b-x+0_2'}, {'s-x+0_1', 'b-x+1_2', 'b-y+2_0', 'd-y+1_2', 'no_title', 'b-y+1_0', 'b-x+0_2'}, {'b-x+1_2', 'b-y+2_0', 'b-x+0_2', 'd-y+1_2', 's-x+1_0', 'b-y+1_0', 'title+0'}]
,3)
BACKGROUND_QUOTE_LEARNED=([{'background+1', 'd-y+0_1', 'no_title', 'd-x+0_1'}],2)
BACKGROUND_ONLY_LEARNED=([{'no_title', 'background+0'}],1)
ARCHETYPES_LEARNED=[TITLE_SLIDE_LEARNED,TITLE_SINGLE_CONTENT_LEARNED,TITLE_DOUBLE_CONTENT_LEARNED,TITLE_TRIPLE_CONTENT_LEARNED,COMPARISON_LEARNED,SECTION_HEADER_LEARNED,TITLE_ONLY_LEARNED,CAPTIONED_CONTENT_LEARNED,BACKGROUND_QUOTE_LEARNED,BACKGROUND_ONLY_LEARNED]

def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    return float(intersection) / max((len(list1) + len(list2)) - intersection,1)

def evaluate_mapping(enc,mapping):
    new_enc=set()
    for i in enc:
        if i=="first_slide" or i=="no_title" or i=="no_content":
            new_enc.add(i)
        else:
            plus_index=i.index("+")+1
            numbers=i[plus_index:]
            if "_" in numbers:
                line_index=numbers.index("_")
                number1=numbers[:line_index]
                number2=numbers[line_index+1:]
                if number1 not in mapping.keys():
                    mapping[number1]=number1
                if number2 not in mapping.keys():
                    mapping[number2]=number2
                new_enc.add(i[:plus_index]+mapping[number1]+"_"+mapping[number2])
            else:
                if numbers not in mapping.keys():
                    mapping[numbers]=numbers
                new_enc.add(i[:plus_index] + mapping[numbers])
    return new_enc

def get_mappings(title1,title2,n1,n2):
    mappings=[]
    range_1=range(0,n1)
    permutations = list(itertools.permutations(range_1,n2))
    for perm in permutations:
        mapping={}
        for i in range(0,n2):
            mapping[str(i)]=str(perm[i])
        mappings.append(mapping)
    if title1!=None and title2!=None:
        mappings=[x for x in mappings if x[str(title2)]==str(title1)]
    return mappings


def get_full_mappings(enc1,enc2,n1,n2):
    mappings = []
    range_1 = range(0,n1)
    permutations = list(itertools.permutations(range_1, n2))
    possibilities={}
    possibilities2={}
    for i in enc2:
        if "first_slide" not in i and "no_content" not in i and "no_title" not in i:
            if "_" in i:
                if i[:-3] in possibilities.keys():
                    possibilities[i[:-3]].append((int(i[-3]),int(i[-1])))
                else:
                    possibilities[i[:-3]]=[((int(i[-3]), int(i[-1])))]
            else:
                if i[:-1] in possibilities.keys():
                    possibilities[i[:-1]].append((int(i[-1]),))
                else:
                    possibilities[i[:-1]]=[(int(i[-1]),)]
    for i in enc1:
        if "first_slide" not in i and "no_content" not in i and "no_title" not in i:
            if "_" in i:
                if i[:-3] in possibilities2.keys():
                    possibilities2[i[:-3]].append((int(i[-3]),int(i[-1])))
                else:
                    possibilities2[i[:-3]]=[((int(i[-3]), int(i[-1])))]
            else:
                if i[:-1] in possibilities2.keys():
                    possibilities2[i[:-1]].append((int(i[-1]),))
                else:
                    possibilities2[i[:-1]]=[(int(i[-1]),)]
    possible_combinations=set()
    for i in possibilities.keys()&possibilities2.keys():
        val1=possibilities[i]
        val2=possibilities2[i]
        x1=set([x[0] for x in val1])
        x2=set([x[0] for x in val2])
        for comb in list(itertools.product(x1,x2)):
            possible_combinations.add(comb)
        if len(val1[0])>1:
            y1 = set([x[1] for x in val1])
            y2 = set([x[1] for x in val2])
            for comb in list(itertools.product(y1,y2)):
                possible_combinations.add(comb)
    for perm in permutations:
        mapping={}
        possible=True
        for i in range(0,n2):
            if (i,perm[i]) not in possible_combinations:
                possible=False
            mapping[str(i)]=str(perm[i])
        if possible:
            mappings.append(mapping)
    return mappings



@lru_cache(maxsize=100000, typed=False)
def optimal_substitution(in_enc1,in_enc2,in_n1,in_n2):
    #enc1 is always the longest
    if in_n1>=in_n2:
        enc1=in_enc1
        enc2=in_enc2
        n1=in_n1
        n2=in_n2
    else:
        enc1=in_enc2
        enc2=in_enc1
        n1 = in_n2
        n2 = in_n1
    max_dist=jaccard(enc1,enc2)
    mapping_standard={}
    for i in range(0,n1):
        mapping_standard[str(i)]=str(i)
    if max_dist==1.0:
        return 1.0,True,mapping_standard
    # elif in_n2<=in_n1 and jaccard(enc2,enc1&enc2)==1.0:
    #     return max_dist,True,mapping_standard
    else:
        best_mapping={}
        # title1=None
        # title2=None
        # for i in range(0,n1):
        #     if "title+"+str(i) in enc1:
        #         title1=i
        #     if "title+"+str(i) in enc2:
        #         title2=i

        for mapping in get_full_mappings(frozenset(enc1),frozenset(enc2),n1,n2):#get_mappings(title1,title2,n1,n2):
            if mapping!=mapping_standard:
                new_enc=evaluate_mapping(enc2,mapping)
                new_jacard=jaccard(enc1,new_enc)
                if max_dist<new_jacard:
                    max_dist=new_jacard
                    best_mapping=mapping

                if max_dist==1.0:# or (in_n2<=in_n1 and jaccard(new_enc,enc1&new_enc)==1.0):
                    if n1>n2:
                        reversed_mapping = {}
                        for i in mapping.keys():
                            reversed_mapping[mapping[i]] = i
                        for i in range(0,n1):
                            if str(i) not in reversed_mapping.keys():
                                reversed_mapping[str(i)]=str(len(reversed_mapping))
                        mapping=reversed_mapping
                    return max_dist, True,mapping
    if n1 > n2:
        reversed_mapping = {}
        for i in best_mapping.keys():
            reversed_mapping[best_mapping[i]] = i
        for i in range(0, n1):
            if str(i) not in reversed_mapping.keys():
                reversed_mapping[str(i)] = str(len(reversed_mapping))
        best_mapping = reversed_mapping
    return max_dist,False, best_mapping


def RA2archetype(powerpoint, arch_to_use, cutoff):
    """"
    De functie die een slideshow uitgedrukt in RA-algebra omzet naar archetypes.
    Deze archetypes zijn de basisvormen van de uiteindelijke powerpoint. Deze functie geeft archetype-objecten terug
    met daarin de juiste geanoteerde content_indexes die later samen met de categorized xml terug de slide kunnen opbouwen."""
    archs_to_use=[([x[0]],x[1]) for x in ARCHETYPES]
    if arch_to_use=="baseline":
        archs_to_use=[([x[0]],x[1]) for x in ARCHETYPES_RA]
    elif arch_to_use=="overlap":
        archs_to_use=[([x[0]],x[1]) for x in ARCHETYPES]
    elif arch_to_use=="learned":
        archs_to_use=ARCHETYPES_LEARNED
    archetypes=[]
    total_pages=len(powerpoint.pages)
    count=1
    for page in powerpoint.pages:
        print(count, total_pages)
        count+=1
        print(page.RA)
        archetype,simil= find_archetype(page.RA,page.n, True,archs_to_use, cutoff)
        print(archetype,simil)
        archetypes.append(archetype)
    return archetypes,[]

def remove_overlapping(RA_set):
    n=RA_set[1]
    RA_list=list(RA_set[0])
    lists=[RA_list]
    while "overlapping" in str(lists[0]):
        new_lists=[]
        for lijst in lists:
            index = [idx for idx, s in enumerate(lijst) if 'overlapping' in s][0]
            el = lijst.pop(index)
            if el.startswith("not_overlapping"):
                numbers=el[15:]
                for rel in NOT_OVERLAPPING:
                    new_lists.append(lijst+[rel+numbers])
            else:
                numbers = el[11:]
                for rel in OVERLAPPING:
                    new_lists.append(lijst+[rel+numbers])
        lists=new_lists[:]
    return [(set(l),n) for l in lists]

def find_archetype(RA,n, recursive, archs_to_use, cutoff=0):

    """"
    De functie die voor een bepaalde slide (gegeven door de RA-matrix) het archetype bepaald. Dit gaat als volgt:
    1. er worden een aantal constraints bepaald
    2. Als een slide een een correcte combinatie van constraints voldoet is het dat archetype
    3. als dit niet het geval is wordt er via een breadth-first-search een nieuwe RA opgesteld waarvoor terug een archetype gezocht wordt"""
    best_simil=0
    best_archetype=None
    best_mapping=None
    if n>8:
        return ContentOnly(range(0,n)),0
    for index in range(0,len(archs_to_use)):
        #remove_overlapping(ARCHETYPES[index]):
        archie = archs_to_use[index]
        archetype=archie[0]
        archetype_length=archie[1]
        for arch in archetype:
            dist,solution,mapping=optimal_substitution(frozenset(RA),frozenset(arch),n,archetype_length)
            if solution:
               return make_archetype(index,n,mapping, RA),dist
        if solution and dist > best_simil:
            best_simil = dist
            best_archetype = index
            best_mapping = mapping

    if best_archetype!=None:
        return make_archetype(best_archetype,n,best_mapping, RA),best_simil
    elif recursive:
        print("closest")
        return select_closest(RA,n, archs_to_use, cutoff)
    else:
        return None,0
def make_archetype(archetype,n,mapping, RA):
    reversed_mapping={}
    for i in mapping.keys():
        reversed_mapping[mapping[i]]=i
    #Titleslide
    if archetype==0:
        title_index = reversed_mapping["0"]
        subtext=[]
        for index in range(0,n):
            if "bi-y+"+title_index+"_"+str(index) in RA and "overlapping-x+"+title_index+"_"+str(index) in RA:
                subtext.append(index)
        return TitleSlide(int(title_index),subtext)

    #Title single content
    elif archetype==1:
        title_index = reversed_mapping["0"]
        single_content=reversed_mapping["1"]
        return TitleSingleContent(int(title_index),int(single_content))
    #Title double content
    elif archetype==2:
        title_index=reversed_mapping["0"]
        double_content_1=reversed_mapping["1"]
        double_content_2=reversed_mapping["2"]
        if "b-x+"+double_content_1+"_"+double_content_2 in RA or "m-x+"+double_content_1+"_"+double_content_2 in RA:
            return TitleDoubleContent(int(title_index),int(double_content_1),int(double_content_2))
        else:
            return TitleDoubleContent(int(title_index),int(double_content_2),int(double_content_1))
    #Title triple content
    elif archetype==3:
        title_index = reversed_mapping["0"]
        triple_content_1 = reversed_mapping["1"]
        triple_content_2 = reversed_mapping["2"]
        triple_content_3 = reversed_mapping["3"]
        permutations = set(itertools.permutations([triple_content_1,triple_content_2,triple_content_3]))
        for i in permutations:
            if ("b-x+" + i[0] + "_" + i[1] in RA or "m-x+" + i[0] + "_" + i[1] in RA) and ("b-x+" + i[1] + "_" + i[2] in RA or "m-x+" + i[1] + "_" + i[2] in RA):
                return TitleTripleContent(int(title_index), int(i[0]), int(i[1]),int(i[2]))
        return TitleTripleContent(int(title_index),triple_content_1,triple_content_2,triple_content_3)
    #Comparison
    elif archetype==4:
        title_index = reversed_mapping["0"]
        double_content_1 = reversed_mapping["1"]
        double_content_2 = reversed_mapping["2"]
        double_subcontent_1=reversed_mapping["3"]
        double_subcontent_2 = reversed_mapping["4"]
        if "b-x+" + double_content_1 + "_" + double_content_2 in RA or "m-x+" + double_content_1 + "_" + double_content_2 in RA:
            if "b-x+" + double_subcontent_1 + "_" + double_subcontent_2 in RA or "m-x+" + double_subcontent_1 + "_" + double_subcontent_2 in RA:
                return Comparison(int(title_index), int(double_content_1), int(double_content_2), int(double_subcontent_1),int(double_subcontent_2))
            else:
                return Comparison(int(title_index), int(double_content_1), int(double_content_2), int(double_subcontent_2),int(double_subcontent_1))
        else:
            if "b-x+" + double_subcontent_1 + "_" + double_subcontent_2 in RA or "m-x+" + double_subcontent_1 + "_" + double_subcontent_2 in RA:
                return Comparison(int(title_index), int(double_content_2), int(double_content_1), int(double_subcontent_1),int(double_subcontent_2))
            else:
                return Comparison(int(title_index), int(double_content_2), int(double_content_1), int(double_subcontent_2),int(double_subcontent_1))
    #Section header
    elif archetype==5:
        title_index = reversed_mapping["0"]
        subtext = []
        for index in range(0, n):
            if "bi-y+" + title_index + "_" + str(index) in RA and "overlapping-x+" + title_index + "_" + str(
                    index) in RA:
                subtext.append(index)
        return SectionHeader(int(title_index), subtext)

    #Title Only
    elif archetype==6:
        title_index = reversed_mapping["0"]
        return TitleOnly(int(title_index))
    #Captioned Content
    elif archetype==7:
        left_up=reversed_mapping["0"]
        left_down=reversed_mapping["1"]
        right=reversed_mapping["2"]
        return CaptionedContent(int(left_up),int(left_down),int(right))
    #Background Quote
    elif archetype==8:
        title=reversed_mapping["0"]
        background=reversed_mapping["1"]
        return BackgroundQuote(int(title),int(background))
    #Background Only
    elif archetype==9:
        background=reversed_mapping["0"]
        return BackgroundOnly(int(background))

def change_overlapping(relation):
    """functie die gebruik makend van een bepaalde relatie de switch maakt voor de breadth first search"""
    if relation =="middelboven":
        return "middelboven"
    elif relation =="middelmiddel":
        return "middelmiddel"
    elif relation in ["linksboven","rechtsboven"]:
        return "middelboven"
    elif relation in ["linksmiddel","rechtsmiddel","linksonder","middelonder","rechtsonder"]:
        return "middelmiddel"
    elif relation=="overlapping":
        return "not_overlapping"
    elif relation=="not_overlapping":
        return "overlapping"
    else:
        if relation in NOT_OVERLAPPING:
            if "i" not in relation:
                return "di"
            else:
                return "d"
        else:
            if "i" not in relation:
                return "bi"
            else:
                return "b"

def change_overlapping_full(all_changes,combo,new_RA, amount, archs, cutoff):
    positions = ["middelmiddel", "middelboven", "rechtsboven", "rechtsmiddel", "rechtsonder", "middelonder",
                 "linksonder", "linksmiddel", "linksboven"]
    relations = ["b", "m", "o", "d", "s", "f", "eq"]#, "fi", "si", "di", "oi", "mi", "bi"]
    binary_indices_to_change=[]
    single_indices_to_change=[]
    for i in range(0,len(new_RA)):
        relation=new_RA[i]
        if "background" not in relation and "title" not in relation and "content" not in relation and "first_slide" not in relation:
            numbers = relation[relation.find("+") + 1:]
            # if "_" not in numbers:
            #     single_change = int(numbers)
            #     if (single_change, single_change) in all_changes:
            #         single_indices_to_change.append(i)
            # else:
            change_1 = int(numbers[:numbers.find("_")])
            change_2 = int(numbers[numbers.find("_") + 1:])
            if (change_1, change_2) in all_changes or (change_2, change_1) in all_changes:
                if (change_1, change_2) in all_changes:
                    z = combo[all_changes.index((change_1, change_2))]
                else:
                    z = combo[all_changes.index((change_2, change_1))]
                if z % 2 == 0 and "-x" in relation:
                    binary_indices_to_change.append(i)
                if z > 0 and "-y" in relation:
                    binary_indices_to_change.append(i)
    combinations=[]
    # for i in single_indices_to_change:
    #     combinations.append([(i,x) for x in range(0,9) if x!=positions.index(new_RA[i][:-2])])
    for i in binary_indices_to_change:
        combinations.append([(i,x) for x in range(0,7) if x!=relations.index(new_RA[i][:-6])])
    best_simil=0
    best_arch=None
    for change in itertools.product(*combinations):
        z=new_RA[:]
        for i in change:
            element=new_RA[i[0]]
            if "_" in element:
                z[i[0]]=relations[i[1]]+element[-6:]
            else:
                z[i[0]] = positions[i[1]] + element[-2:]
        archetype,simil = find_archetype(set(z), amount, False, archs)
        if simil==1:
            return archetype,1
        if simil>=best_simil:
            best_simil=simil
            best_arch=archetype
    return best_arch,best_simil

from datetime import datetime
def select_closest(RA_set,amount, archs, cutoff):

    """
   Iterative deepening op de RA-matrix
    """
    #aantal elementen in de bovendriehoeksmatrix
    max_amount_changes = int(amount + (amount * amount - amount) / 2)
    extra = 0
    mapping = {}
    #mapping van single getal naar extra getal om bovendriehoek om te zetten
    for i in range(0, max_amount_changes):
        if (i + sum(range(0, extra + 1))) % amount == 0 and i > 0:
            extra += 1
        mapping[i] = extra

    for amount_changes in range(1, max_amount_changes+1):
        if amount_changes>cutoff:
            return ContentOnly(range(0,amount)),0
        #alle combinaties om linker, rechter en beide relaties om te zetten: bvb:
        combinations = [z for v in [set(itertools.permutations(x)) for x in
                                    list(itertools.combinations_with_replacement(range(0, 3), amount_changes))] for z in
                        v]
        possible_changes=list(set(itertools.combinations(range(0, max_amount_changes), amount_changes)))
        best_simil=0
        best_arch=None
        for changes_index in range(0,len(possible_changes)):
            changes=possible_changes[changes_index]
            all_changes = []
            for change in changes:
                extra = sum(range(0, mapping[change] + 1))
                x_index = (change + extra) // amount
                y_index = (change + extra) % amount
                all_changes.append((x_index, y_index))
            for combo in combinations:
                # resolve 1 combination of changes
                new_RA = list(RA_set)
                archetype, simil=change_overlapping_full(all_changes,combo,new_RA,amount, archs, cutoff)
                if simil==1:
                    return archetype,simil
                if simil>=best_simil and archetype!=None:
                    best_simil=simil
                    best_arch=archetype
        if best_arch!=None:
            return best_arch,best_simil
                # for i in range(0, len(new_RA)):
                #     relation = new_RA[i]
                #     if "background" not in relation and "title" not in relation and "content" not in relation and "first_slide" not in relation:
                #         numbers=relation[relation.find("+")+1:]
                #         if "_" not in numbers:
                #             single_change=int(numbers)
                #             if (single_change,single_change) in all_changes:
                #                 new_RA[i]=change_overlapping(relation[:-2])+relation[-2:]
                #         else:
                #             change_1=int(numbers[:numbers.find("_")])
                #             change_2 = int(numbers[numbers.find("_")+1:])
                #
                #             if (change_1,change_2) in all_changes or (change_2,change_1) in all_changes:
                #                 skip=relation.find("-")
                #                 if (change_1, change_2) in all_changes:
                #                     z=combo[all_changes.index((change_1, change_2))]
                #                 else:
                #                     z = combo[all_changes.index((change_2, change_1))]
                #                 if z % 2 == 0 and "-x" in relation:
                #                     new_RA[i]=change_overlapping(relation[:skip])+relation[skip:]
                #                 if z > 0 and "-y" in relation:
                #                     new_RA[i] = change_overlapping(relation[:skip]) + relation[skip:]
                # archetype = find_archetype(set(new_RA), amount, False)
                # if archetype!=None:
                #     # with open("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\clustering\\clusters.txt",'a') as f:
                #     #     if len(RA_set)>0:
                #     #         f.write(str((RA_set,amount))+"\n")
                #     return archetype
    # with open("D:\\User\\Documents\\School\\Thesis\\thesis_sieben_bocklandt\\Data\\clustering\\clusters.txt",'a') as f:
    #     if len(RA_set) > 0:
    #         f.write(str((RA_set, amount)) + "\n")

    return ContentOnly(range(0,amount)),0


