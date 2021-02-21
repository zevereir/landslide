import json
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.interpolate import make_interp_spline, BSpline
import pandas as pd

all=['1_128_6.png265565', '3_512_12.png106278', '4_396_5.png202920', '6_400_16.png228998', '7_525_26.png112301', '8_177_7.png183675', '9_177_11.png312510', '10_119_9.png298081', '11_111_10.png132503', '12_463_110.png310695', '13_90_15.png180183', '15_277_60.png268154', '16_456_1.png105161', '17_236_6.png62861', '18_115_0.png100201', '21_307_6.png272804', '25_87_28.png117728', '26_37_25.png39610', '28_572_23.png462170', '29_620_19.png157925', '30_506_16.png319135', '31_180_26.png279119', '32_463_104.png166198', '33_625_2.png299446', '34_358_7.png125573', '35_379_7.png188218', '36_24_8.png129232', '37_215_3.png346414', '39_531_98.png85444', '40_358_49.png186932', '41_108_9.png80308', '42_525_0.png79943', '43_125_5.png232445', '44_328_51.png176631', '46_330_4.png208713', '47_181_3.png415854', '48_439_20.png309816', '49_515_2.png280740', '50_254_7.png78987', '51_431_3.png298431', '52_235_6.png161969', '53_79_16.png209818', '54_71_12.png425787', '55_615_16.png82203', '56_107_24.png49608', '57_549_28.png80844', '59_247_2.png330261', '60_438_7.png208540', '61_76_11.png83607', '63_400_17.png221046', '64_104_39.png174157', '65_604_30.png126664', '66_325_3.png138534', '67_473_24.png240036', '68_387_21.png153727', '70_201_12.png217591', '71_358_4.png220115', '72_194_1.png510097', '73_54_17.png85074', '74_131_21.png162412', '75_41_74.png185328', '77_177_0.png206015', '78_523_28.png53246', '79_235_13.png140116', '80_54_37.png360765', '82_609_21.png208641', '83_37_46.png122957', '84_465_14.png412200', '86_398_17.png319377', '87_479_4.png294015', '88_520_15.png187613', '90_150_36.png118224', '91_349_5.png185669', '92_469_25.png291721', '93_251_11.png122364', '94_120_4.png128795', '95_79_9.png172459', '96_570_211.png192489', '97_83_21.png162997', '98_290_12.png84958', '99_311_11.png128345', '101_574_50.png179363', '102_225_1.png873591', '103_490_5.png281758', '104_441_7.png218114', '105_271_2.png254095', '107_421_6.png152587', '108_218_3.png111315', '109_562_1.png342475', '110_557_8.png34095', '111_264_4.png168317', '112_477_14.png229264', '113_385_4.png136744', '114_575_7.png220930', '115_543_36.png300628', '117_622_19.png256915', '118_335_6.png228807', '120_285_6.png158423', '121_489_17.png186995', '122_568_7.png319156', '123_474_4.png88651', '125_194_35.png462261', '126_54_34.png381967', '127_627_7.png149714', '128_556_41.png136631', '130_50_16.png288363', '131_370_5.png202230', '132_300_6.png178612', '133_495_6.png98863', '135_328_15.png197687', '137_269_7.png246527', '138_249_2.png78236', '139_11_49.png205590', '140_411_17.png168159', '141_469_34.png274512', '142_458_4.png75471', '143_57_9.png90387', '144_157_13.png182122', '145_572_0.png614617', '147_310_4.png64520', '148_63_0.png305060', '149_229_23.png147870', '150_629_37.png153188', '152_145_62.png670040', '153_305_12.png193999', '154_7_4.png215158', '156_520_33.png191640', '157_50_11.png136286', '158_532_13.png97177', '159_233_31.png497952', '160_267_7.png102966', '161_41_142.png102533', '162_533_26.png442535', '163_264_12.png210541', '164_63_11.png179872', '165_279_9.png98493', '166_425_19.png202289', '167_548_12.png167940', '168_426_70.png170548', '170_278_0.png64060', '171_52_8.png164864', '172_529_23.png57021', '173_402_3.png245577', '174_523_33.png18462', '176_579_8.png336896', '177_97_19.png243018', '179_158_1.png262885', '180_531_47.png150236', '181_555_61.png141463', '182_197_0.png215341', '183_64_4.png69366', '184_194_32.png454983', '185_265_19.png205263', '186_615_2.png207989', '187_397_6.png181434', '188_221_2.png72437', '189_41_168.png108118', '191_412_1.png208867', '192_524_22.png162220', '195_285_17.png157083', '196_224_70.png195338', '197_20_12.png198670', '200_412_8.png371165', '201_89_5.png96731', '202_13_2.png167794', '203_513_27.png131254', '204_487_1.png87746', '205_463_12.png251399', '206_628_51.png104986', '207_251_0.png152751', '208_232_6.png79352', '209_3_37.png152343', '210_265_22.png291293', '211_610_8.png258996', '212_288_50.png160718', '213_319_25.png105467', '214_67_8.png291574', '215_462_36.png379217', '216_154_3.png217426', '217_433_79.png189719', '218_41_208.png196127', '219_541_20.png179292', '220_629_22.png126593', '221_83_6.png106898', '222_529_34.png181541', '223_144_13.png114129', '224_570_159.png163218', '226_231_0.png148935', '229_566_14.png512205', '230_288_6.png242305', '232_288_41.png137200', '233_293_9.png216622', '234_391_10.png278003', '236_525_21.png124760', '238_54_3.png402584', '239_356_2.png281494', '240_229_27.png246667', '242_179_5.png342489', '243_310_12.png167335', '244_104_14.png186669', '245_451_20.png135124', '246_74_19.png469348', '248_517_17.png320434', '249_41_278.png187335', '250_411_0.png77983', '251_37_35.png101130', '253_217_13.png222779', '254_108_1.png91735', '255_224_82.png235857', '256_376_3.png147463', '257_570_178.png211608', '258_518_4.png145623', '259_330_16.png90212', '261_63_3.png147888', '262_436_42.png248472', '263_253_20.png193001', '264_265_0.png179263', '265_628_36.png117790', '266_524_4.png139164', '267_419_27.png184713', '268_301_3.png104067', '269_184_2.png144009', '270_347_27.png465604', '271_48_6.png220265', '272_156_14.png118828', '273_368_2.png201220', '274_370_0.png93321', '275_281_7.png215397', '276_243_9.png184211', '277_568_5.png438809', '279_161_29.png114276', '280_570_200.png37413', '281_194_30.png512884', '283_330_8.png198530', '284_439_13.png314713', '285_305_31.png155018', '286_54_0.png358744', '287_474_7.png83973', '288_149_16.png170063', '289_11_22.png173290', '291_570_273.png211091', '292_229_26.png134082', '293_396_22.png151220', '294_439_5.png290222', '296_445_31.png364777', '297_251_39.png135632', '298_609_7.png216676', '299_555_67.png173690', '300_129_9.png298081', '301_10_9.png283455', '302_346_14.png129917', '303_106_9.png268055', '304_54_38.png222464', '305_499_8.png348209', '306_561_2.png262608', '307_268_12.png109207', '308_412_17.png267673', '309_628_12.png134193', '310_628_10.png121849', '311_502_11.png154000', '312_208_7.png114719', '313_355_7.png145896', '314_380_45.png115277', '316_287_9.png18542', '317_128_23.png209482', '318_86_18.png110177', '319_513_2.png183947', '320_67_14.png305198', '321_463_26.png237213', '322_162_21.png104889', '323_417_10.png480194', '324_113_14.png10248', '325_307_14.png213171', '326_524_35.png163857', '327_161_23.png148330', '328_604_47.png136903', '329_517_2.png314630', '330_362_1.png164622', '332_490_0.png211330', '333_387_65.png293498', '334_224_140.png286977', '335_110_5.png193620', '336_414_36.png214377', '337_285_2.png224713', '338_285_10.png334267', '340_41_27.png113884', '342_434_49.png272400', '343_555_5.png161958', '344_362_10.png143377', '345_513_6.png117313', '347_218_16.png214883', '348_316_26.png337701', '349_102_10.png127393', '350_228_10.png40700', '352_452_7.png138891', '353_114_13.png113189', '354_59_1.png211766', '355_111_15.png107789', '356_570_126.png101436', '358_69_4.png176567', '359_224_74.png192052', '361_182_12.png237797', '362_570_276.png210890', '363_429_16.png134528', '365_36_10.png127393', '367_146_33.png179781', '369_419_36.png171153', '370_77_11.png82924', '371_565_11.png219360', '372_78_0.png104895', '373_397_13.png256838', '374_553_5.png268929', '375_570_258.png191338', '378_291_5.png278226', '380_192_0.png158811', '381_429_2.png224783', '382_41_276.png210890', '383_473_16.png224904', '384_605_15.png370468', '385_57_8.png75303', '386_58_1.png186174', '387_310_55.png73890', '388_127_10.png268437', '389_543_14.png149331', '391_457_15.png312181', '393_459_31.png250158', '396_57_1.png177604', '397_459_47.png591110', '398_549_5.png205075', '399_129_12.png41779', '400_55_10.png119019', '401_168_17.png132387', '402_476_3.png302023', '403_92_2.png104548', '404_469_6.png162608', '405_562_25.png235078', '406_615_11.png168120', '407_44_10.png206374', '409_288_10.png43103', '410_404_3.png158920', '411_310_54.png64994', '412_451_2.png79236', '414_233_2.png165253', '415_212_8.png536746', '416_37_42.png104934', '419_604_69.png115044', '420_19_3.png150858', '421_556_14.png278829', '422_217_24.png357665', '423_167_46.png233149', '424_15_23.png194958', '426_385_3.png153447', '427_321_9.png173489', '428_552_1.png244984', '430_526_6.png79614', '431_273_12.png147332', '432_417_11.png463675', '433_437_6.png174208', '434_298_12.png120096', '435_628_19.png144414', '436_307_16.png208576', '437_224_144.png187641', '438_175_5.png156208', '439_258_11.png203580', '440_89_70.png100354', '441_507_10.png134127', '443_429_1.png107946', '444_14_9.png261061', '445_155_42.png105682', '446_524_17.png138180', '447_555_29.png39234', '448_90_3.png228935', '449_463_93.png177514', '451_140_29.png149208', '452_312_22.png149773', '455_159_2.png132605', '456_435_8.png198073', '457_64_28.png181109', '458_319_2.png277805', '459_426_22.png235228', '460_337_17.png174277', '462_288_18.png54808', '464_607_6.png136516', '465_243_94.png293383', '467_118_12.png174856', '468_306_3.png103426', '469_511_0.png143454', '470_371_5.png55236', '471_531_111.png54905', '472_314_52.png216992', '473_118_7.png161737', '474_583_13.png174576', '475_36_3.png130511', '476_207_18.png397025', '479_68_12.png196283', '480_436_31.png193025', '481_37_44.png192221', '482_512_14.png87874', '483_228_32.png139598', '484_301_2.png106591', '485_624_22.png208281', '487_555_36.png75627', '488_494_49.png365830', '489_126_3.png145169', '491_396_6.png102512', '494_373_0.png133430', '496_348_28.png250915', '497_385_25.png210872', '498_107_13.png193401']
equal=['1_128_6.png265565', '3_512_12.png106278', '8_177_7.png183675', '9_177_11.png312510', '10_119_9.png298081', '11_111_10.png132503', '12_463_110.png310695', '15_277_60.png268154', '17_236_6.png62861', '18_115_0.png100201', '21_307_6.png272804', '25_87_28.png117728', '26_37_25.png39610', '28_572_23.png462170', '29_620_19.png157925', '30_506_16.png319135', '31_180_26.png279119', '32_463_104.png166198', '33_625_2.png299446', '34_358_7.png125573', '35_379_7.png188218', '36_24_8.png129232', '37_215_3.png346414', '39_531_98.png85444', '40_358_49.png186932', '41_108_9.png80308', '42_525_0.png79943', '43_125_5.png232445', '44_328_51.png176631', '46_330_4.png208713', '47_181_3.png415854', '48_439_20.png309816', '50_254_7.png78987', '51_431_3.png298431', '52_235_6.png161969', '53_79_16.png209818', '54_71_12.png425787', '55_615_16.png82203', '56_107_24.png49608', '57_549_28.png80844', '59_247_2.png330261', '60_438_7.png208540', '61_76_11.png83607', '66_325_3.png138534', '68_387_21.png153727', '70_201_12.png217591', '71_358_4.png220115', '72_194_1.png510097', '74_131_21.png162412', '77_177_0.png206015', '78_523_28.png53246', '79_235_13.png140116', '83_37_46.png122957', '87_479_4.png294015', '88_520_15.png187613', '90_150_36.png118224', '92_469_25.png291721', '93_251_11.png122364', '94_120_4.png128795', '95_79_9.png172459', '96_570_211.png192489', '97_83_21.png162997', '98_290_12.png84958', '99_311_11.png128345', '101_574_50.png179363', '103_490_5.png281758', '104_441_7.png218114', '105_271_2.png254095', '108_218_3.png111315', '109_562_1.png342475', '110_557_8.png34095', '111_264_4.png168317', '112_477_14.png229264', '113_385_4.png136744', '114_575_7.png220930', '115_543_36.png300628', '118_335_6.png228807', '120_285_6.png158423', '121_489_17.png186995', '122_568_7.png319156', '123_474_4.png88651', '127_627_7.png149714', '128_556_41.png136631', '130_50_16.png288363', '132_300_6.png178612', '133_495_6.png98863', '135_328_15.png197687', '137_269_7.png246527', '138_249_2.png78236', '139_11_49.png205590', '140_411_17.png168159', '142_458_4.png75471', '143_57_9.png90387', '144_157_13.png182122', '145_572_0.png614617', '147_310_4.png64520', '149_229_23.png147870', '150_629_37.png153188', '153_305_12.png193999', '154_7_4.png215158', '156_520_33.png191640', '157_50_11.png136286', '158_532_13.png97177', '159_233_31.png497952', '161_41_142.png102533', '164_63_11.png179872', '165_279_9.png98493', '167_548_12.png167940', '168_426_70.png170548', '170_278_0.png64060', '171_52_8.png164864', '172_529_23.png57021', '173_402_3.png245577', '174_523_33.png18462', '176_579_8.png336896', '179_158_1.png262885', '180_531_47.png150236', '183_64_4.png69366', '185_265_19.png205263', '186_615_2.png207989', '188_221_2.png72437', '189_41_168.png108118', '191_412_1.png208867', '192_524_22.png162220', '195_285_17.png157083', '196_224_70.png195338', '197_20_12.png198670', '201_89_5.png96731', '202_13_2.png167794', '203_513_27.png131254', '204_487_1.png87746', '205_463_12.png251399', '206_628_51.png104986', '207_251_0.png152751', '208_232_6.png79352', '209_3_37.png152343', '210_265_22.png291293', '211_610_8.png258996', '212_288_50.png160718', '216_154_3.png217426', '218_41_208.png196127', '219_541_20.png179292', '220_629_22.png126593', '221_83_6.png106898', '222_529_34.png181541', '223_144_13.png114129', '224_570_159.png163218', '226_231_0.png148935', '229_566_14.png512205', '233_293_9.png216622', '234_391_10.png278003', '236_525_21.png124760', '239_356_2.png281494', '242_179_5.png342489', '243_310_12.png167335', '244_104_14.png186669', '245_451_20.png135124', '246_74_19.png469348', '249_41_278.png187335', '250_411_0.png77983', '251_37_35.png101130', '253_217_13.png222779', '254_108_1.png91735', '255_224_82.png235857', '257_570_178.png211608', '258_518_4.png145623', '259_330_16.png90212', '261_63_3.png147888', '262_436_42.png248472', '263_253_20.png193001', '264_265_0.png179263', '265_628_36.png117790', '266_524_4.png139164', '267_419_27.png184713', '268_301_3.png104067', '269_184_2.png144009', '270_347_27.png465604', '271_48_6.png220265', '272_156_14.png118828', '273_368_2.png201220', '274_370_0.png93321', '275_281_7.png215397', '276_243_9.png184211', '277_568_5.png438809', '280_570_200.png37413', '283_330_8.png198530', '285_305_31.png155018', '287_474_7.png83973', '288_149_16.png170063', '289_11_22.png173290', '293_396_22.png151220', '294_439_5.png290222', '296_445_31.png364777', '297_251_39.png135632', '298_609_7.png216676', '299_555_67.png173690', '300_129_9.png298081', '301_10_9.png283455', '302_346_14.png129917', '303_106_9.png268055', '304_54_38.png222464', '305_499_8.png348209', '306_561_2.png262608', '307_268_12.png109207', '309_628_12.png134193', '310_628_10.png121849', '311_502_11.png154000', '312_208_7.png114719', '313_355_7.png145896', '314_380_45.png115277', '316_287_9.png18542', '317_128_23.png209482', '318_86_18.png110177', '319_513_2.png183947', '320_67_14.png305198', '321_463_26.png237213', '322_162_21.png104889', '323_417_10.png480194', '324_113_14.png10248', '325_307_14.png213171', '327_161_23.png148330', '328_604_47.png136903', '329_517_2.png314630', '330_362_1.png164622', '332_490_0.png211330', '333_387_65.png293498', '334_224_140.png286977', '335_110_5.png193620', '336_414_36.png214377', '337_285_2.png224713', '340_41_27.png113884', '342_434_49.png272400', '344_362_10.png143377', '345_513_6.png117313', '347_218_16.png214883', '348_316_26.png337701', '349_102_10.png127393', '352_452_7.png138891', '353_114_13.png113189', '354_59_1.png211766', '355_111_15.png107789', '356_570_126.png101436', '358_69_4.png176567', '359_224_74.png192052', '361_182_12.png237797', '362_570_276.png210890', '363_429_16.png134528', '365_36_10.png127393', '367_146_33.png179781', '369_419_36.png171153', '370_77_11.png82924', '371_565_11.png219360', '373_397_13.png256838', '374_553_5.png268929', '375_570_258.png191338', '378_291_5.png278226', '380_192_0.png158811', '382_41_276.png210890', '383_473_16.png224904', '384_605_15.png370468', '385_57_8.png75303', '386_58_1.png186174', '387_310_55.png73890', '388_127_10.png268437', '391_457_15.png312181', '393_459_31.png250158', '396_57_1.png177604', '397_459_47.png591110', '398_549_5.png205075', '399_129_12.png41779', '400_55_10.png119019', '401_168_17.png132387', '402_476_3.png302023', '403_92_2.png104548', '404_469_6.png162608', '405_562_25.png235078', '406_615_11.png168120', '407_44_10.png206374', '409_288_10.png43103', '410_404_3.png158920', '411_310_54.png64994', '412_451_2.png79236', '414_233_2.png165253', '415_212_8.png536746', '416_37_42.png104934', '419_604_69.png115044', '420_19_3.png150858', '421_556_14.png278829', '422_217_24.png357665', '423_167_46.png233149', '424_15_23.png194958', '426_385_3.png153447', '427_321_9.png173489', '428_552_1.png244984', '430_526_6.png79614', '431_273_12.png147332', '432_417_11.png463675', '433_437_6.png174208', '434_298_12.png120096', '435_628_19.png144414', '436_307_16.png208576', '437_224_144.png187641', '438_175_5.png156208', '439_258_11.png203580', '440_89_70.png100354', '441_507_10.png134127', '443_429_1.png107946', '444_14_9.png261061', '446_524_17.png138180', '447_555_29.png39234', '448_90_3.png228935', '449_463_93.png177514', '452_312_22.png149773', '455_159_2.png132605', '456_435_8.png198073', '457_64_28.png181109', '458_319_2.png277805', '459_426_22.png235228', '460_337_17.png174277', '462_288_18.png54808', '464_607_6.png136516', '465_243_94.png293383', '467_118_12.png174856', '468_306_3.png103426', '469_511_0.png143454', '470_371_5.png55236', '471_531_111.png54905', '472_314_52.png216992', '473_118_7.png161737', '474_583_13.png174576', '475_36_3.png130511', '476_207_18.png397025', '479_68_12.png196283', '480_436_31.png193025', '481_37_44.png192221', '482_512_14.png87874', '483_228_32.png139598', '484_301_2.png106591', '485_624_22.png208281', '487_555_36.png75627', '488_494_49.png365830', '489_126_3.png145169', '491_396_6.png102512', '496_348_28.png250915', '497_385_25.png210872', '498_107_13.png193401']
def check_rules(alignment,elements,repr, element):
    if len(elements)==0 or alignment=="TITLE":
        return True
    else:
        if alignment in ["LEFTSUBTITLE","MIDDLESUBTITLE","LEFTCONTENT","MIDDLECONTENT"]:
            for ele in elements:
                if ele[1]=="RIGHTCONTENT" or ele[1]=="RIGHTSUBTITLE":
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  not in ["b","m","o","s","eq"]:

                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  not in ["d","f","eq"]:

                                    return False
        if alignment in ["RIGHTSUBTITLE,MIDDLESUBTITLE","RIGHTCONTENT","MIDDLECONTENT"]:
            for ele in elements:
                if ele[1]=="LEFTCONTENT" or ele[1]=="LEFTSUBTITLE":
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  in ["b","m","o","s"]:

                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-x" in rel:
                                if rel[:rel.find("-")]  in ["d","f"]:

                                    return False

        if "SUBTITLE" in alignment:
            for ele in elements:
                if "CONTENT" in ele[1]:
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  in ["b","m","o","s"]:

                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  in ["d","f"]:

                                    return False
        if "CONTENT" in alignment:
            for ele in elements:
                if "SUBTITLE" in ele[1]:
                    for rel in repr:
                        if "("+str(element)+","+str(ele[0])+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  not in ["b","m","o","s","eq"]:

                                    return False
                        elif "("+str(ele[0])+","+str(element)+")" in rel:
                            if "-y" in rel:
                                if rel[:rel.find("-")]  not in ["d","f","eq"]:

                                    return False
        return True
import os
from pathlib import Path
with open("D:/Thesis/landslide/data/Annotations/alignments.json") as ali:
    alignments=json.load(ali)
with open("D:/Thesis/landslide/data/Annotations/results/annotated_data/roles.json") as rp:
    roles=json.load(rp)
res_path=Path("D:/Thesis/landslide/data/Annotations/results/annotated_data/results/results")
resulting=[]
resulting_equal=[]
resulting_super=[]
confidence=[]
best_practice=(0,None)
for file in os.listdir(res_path):

    with open(res_path/file) as fp:

        results=json.load(fp)
        total_score=0
        total_resp=0
        total_comp=0
        total_score_equal=0
        total_resp_equal=0
        total_comp_equal=0
        total_score_super=0
        total_resp_super=0
        total_comp_super=0
        counter=0
        super_counter=0
        equal_counter=0
        for slide_id in range(1,len(results)+1):

            in_equal = all[slide_id-1] in equal

            # print("----------------------------")

            slide=results[str(slide_id)]
            if slide["Responsitivity"]!=0:
                if in_equal:
                    equal_counter+=1
                else:
                    super_counter+=1
                slide_roles=roles[str(slide_id)]
                total_comp+=slide["Comparisons"]
                #print("Comparisons",slide["Comparisons"])
                if in_equal:
                    total_comp_equal+=slide["Comparisons"]
                else:
                    total_comp_super+=slide["Comparisons"]
                arch=slide["Archetype"]
                mapping=slide["Best mapping"]
                role_mapping=slide["Best role mapping"]
                #print("Responsitivity",slide["Responsitivity"])
                total_resp+=slide["Responsitivity"]
                if not in_equal:
                    total_resp_super+=slide["Responsitivity"]
                else:
                    total_resp_equal+=slide["Responsitivity"]
                # print("Arch",arch)
                # print("Mapping",mapping)
                # print("role_mapping",role_mapping)
                # print("Slide roles",slide_roles)
                if arch<9:
                    pass
                    #print("Alignments",alignments[str(arch)])
                score=0
                # print("Slide = ",slide["New slide"])
                # print("Archetype = ",slide["Archetype representation"])
                # print("MAPPINGS")
                current_mappings=set()
                new_slide=slide["New slide"]
                arch_repr=slide["Archetype representation"]
                slide_repr={x for x in new_slide[11:-2].split(", ")}
                # print(slide_repr)
                for element in range(0,len(slide_roles)):
                    if str(element) in mapping:
                        if str(-mapping[str(element)]) in role_mapping:
                            #print(slide_roles[element] +"--> "+role_mapping[str(-mapping[str(element)])].upper())
                            rule=check_rules(role_mapping[str(-mapping[str(element)])].upper(),current_mappings,slide_repr,element)

                            if slide_roles[element] in alignments[str(arch)][role_mapping[str(-mapping[str(element)])].upper()] and rule:
                                score+=1
                            current_mappings.add((element,role_mapping[str(-mapping[str(element)])].upper()))

                if "background" in new_slide and "background" in arch_repr:
                    ind1=new_slide[new_slide.find("background")+11:new_slide.find("background")+12]
                    ind2=arch_repr[arch_repr.find("background")+11:arch_repr.find("background")+12]
                    if ind1 in mapping and mapping[ind1]==-int(ind2):
                        score+=1
                if len(mapping)==0:
                    total_score+=1
                    if in_equal:
                        total_score_equal+=1
                    else:
                        total_score_super+=1
                    #print(1.0)
                else:
                    #print(score/max(1,len(mapping)))
                    total_score+=(score/max(1,len(mapping)))
                    if in_equal:
                        total_score_equal+=(score/max(1,len(mapping)))
                    else:
                        total_score_super+=(score/max(1,len(mapping)))
                normal={str(x):-x for x in range(0,10)}
                diff=False
                for z in slide["Best mapping"]:
                    if normal[z]!=slide["Best mapping"][z]:
                        diff=True
                transfos=None
                if "Transformations" in slide:
                    transfos=slide["Transformations"]
                    if transfos=="set()":
                        transfos=None
                if score/max(1,len(mapping))==1 and slide["Responsitivity"]==1 and slide_id not in [190,76,143]  and transfos!=None and len(transfos)>best_practice[0]:
                    best_practice=(len(transfos),slide_id, transfos, arch_repr, arch)
    tot=super_counter+equal_counter
    resulting.append((file,total_resp/tot,total_score/tot,total_comp/tot))
    resulting_super.append((file,total_resp_super/super_counter,total_score_super/super_counter,total_comp_super/super_counter))
    resulting_equal.append((file,total_resp_equal/equal_counter,total_score_equal/equal_counter,total_comp_equal/equal_counter))

print("COUNTER",counter)

baseline={}
learned={}
masters={}

for res in resulting:
    if res[0].startswith("greedy"):
        amount=int(res[0][res[0].find("_0_")+3:res[0].find("_F")])
        if "learned" in res[0]:
            if amount in learned:
                learned[amount].append((res[1],res[2],res[3]))
            else:
                learned[amount]=[(res[1],res[2],res[3])]
        elif "baseline" in res[0]:
            if amount in baseline:
                baseline[amount].append((res[1],res[2],res[3]))
            else:
                baseline[amount]=[(res[1],res[2],res[3])]
        elif "masters" in res[0]:
            if amount in masters:
                masters[amount].append((res[1],res[2],res[3]))
            else:
                masters[amount]=[(res[1],res[2],res[3])]

baseline_super={}
learned_super={}
masters_super={}

for res in resulting_super:
    if res[0].startswith("greedy"):
        amount=int(res[0][res[0].find("_0_")+3:res[0].find("_F")])

        if "learned" in res[0]:
            if amount in learned_super:
                learned_super[amount].append((res[1],res[2],res[3]))
            else:
                learned_super[amount]=[(res[1],res[2],res[3])]
        elif "baseline" in res[0]:
            if amount in baseline_super:
                baseline_super[amount].append((res[1],res[2],res[3]))
            else:
                baseline_super[amount]=[(res[1],res[2],res[3])]
        elif "masters" in res[0]:
            if amount in masters_super:

                masters_super[amount].append((res[1],res[2],res[3]))
            else:
                masters_super[amount]=[(res[1],res[2],res[3])]
baseline_equal={}
learned_equal={}
masters_equal={}

for res in resulting_equal:
    if res[0].startswith("greedy"):
        amount=int(res[0][res[0].find("_0_")+3:res[0].find("_F")])
        if "learned" in res[0]:
            if amount in learned_equal:
                learned_equal[amount].append((res[1],res[2],res[3]))
            else:
                learned_equal[amount]=[(res[1],res[2],res[3])]
        elif "baseline" in res[0]:
            if amount in baseline_equal:
                baseline_equal[amount].append((res[1],res[2],res[3]))
            else:
                baseline_equal[amount]=[(res[1],res[2],res[3])]
        elif "masters" in res[0]:
            if amount in masters_equal:

                masters_equal[amount].append((res[1],res[2],res[3]))
            else:
                masters_equal[amount]=[(res[1],res[2],res[3])]
new_baseline=[]
new_learned=[]
new_masters=[]
new_breadth=[]
#
for v in masters:
    z=masters[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    comps=[x[2] for x in z]
    new_masters.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens),comps[0]))
for v in baseline:
    z=baseline[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    comps=[x[2] for x in z]
    new_baseline.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens),comps[0]))
for v in learned:
    z=learned[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    comps=[x[2] for x in z]
    new_learned.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens),comps[0]))

new_baseline_equal=[]
new_learned_equal=[]
new_masters_equal=[]
#
for v in masters_equal:
    z=masters_equal[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    comps=[x[2] for x in z]
    new_masters_equal.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens),comps[0]))
for v in baseline_equal:
    z=baseline_equal[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    comps=[x[2] for x in z]
    new_baseline_equal.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens),comps[0]))
for v in learned_equal:
    z=learned_equal[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    comps=[x[2] for x in z]
    new_learned_equal.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens),comps[0]))
new_baseline_super=[]
new_learned_super=[]
new_masters_super=[]
#
for v in masters_super:
    z=masters_super[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    comps=[x[2] for x in z]
    new_masters_super.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens),comps[0]))
for v in baseline_super:
    z=baseline_super[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    comps=[x[2] for x in z]
    new_baseline_super.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens),comps[0]))
for v in learned_super:
    z=learned_super[v]
    resps=[x[0] for x in z]
    sens=[x[1] for x in z]
    comps=[x[2] for x in z]
    new_learned_super.append((v,min(resps),sum(resps)/len(resps),max(resps),min(sens),sum(sens)/len(sens),max(sens),comps[0]))
#
new_learned.sort()
new_masters.sort()
new_baseline.sort()
new_learned_equal.sort()
new_masters_equal.sort()
new_baseline_equal.sort()
new_learned_super.sort()
new_masters_super.sort()
new_baseline_super.sort()
print(new_baseline)
print(new_learned)
print(new_masters)
for ix in range(0,3):

    i=[new_baseline,new_learned,new_masters,new_baseline_equal,new_learned_equal,new_masters_equal,new_baseline_super,new_learned_super,new_masters_super][ix]
    i=i[0:1]+i[5:7]+i[15:]
    name=["baseline","learned","masters"][ix%3]+["_all","_equal","_super"][ix//3]
    lcolor=["#1b9e77","#d95f02","#7570b3"][ix%3]
    linestyle=["solid","dashed","dotted"][ix//3]

    x_val=[p[0] for p in i]
    print(x_val)
    resp_min=[p[1] for p in i]
    resp_mean=[p[2] for p in i]
    resp_max=[p[3] for p in i]
    sens_min=[p[4] for p in i]
    sens_mean=[p[5] for p in i]
    sens_max=[p[6] for p in i]
    comp=[p[7] for p in i]
    pl=sns.regplot(x="x", y="y",line_kws={'linestyle':linestyle,"lw":2}, data=pd.DataFrame({"x":x_val,"y":resp_mean}),label=name,lowess=True, scatter=True, color=lcolor)
    for wel in range(0,len(comp)):
        wel_vl=comp[wel]
        y_wel=resp_mean[wel]
        plt.scatter(x=wel_vl, y=y_wel, color=lcolor, marker="x")
    #pl.lines[ix]=linestyle
# i=new_breadth
# x_val=[p[0] for p in i]
# resp_min=[p[1] for p in i]
# resp_mean=[p[2] for p in i]
# resp_max=[p[3] for p in i]
# sens_min=[p[4] for p in i]
# sens_mean=[p[5] for p in i]
# sens_max=[p[6] for p in i]
# pl=sns.regplot(x="x", y="y",line_kws={'linestyle':linestyle,"lw":2}, data=pd.DataFrame({"x":x_val,"y":sens_mean}),label="breadth",lowess=True, scatter=False, color="m")


fontP = FontProperties()
fontP.set_size('large')
plt.legend(  loc='lower right', prop=fontP)
plt.show()
figure = pl.get_figure()
# figure.savefig("D:/Thesis/landslide/images_paper/resp_all.svg")





# import json
# import xml.etree.ElementTree as ET
# dict={}
# tree= ET.parse("D://Thesis//landslide//data//Annotations//results//annotated_data//annotated_categorized.xml")
#
# counter=1
# for page in tree.getroot():
#     roles=[]
#     for element in page:
#         roles.append(element.attrib.get("Role"))
#     dict[str(counter)]=roles
#     counter+=1
# with open("D://Thesis//landslide//data//Annotations//results//annotated_data//roles.json","w") as rl:
#     json.dump(dict,rl)
#
