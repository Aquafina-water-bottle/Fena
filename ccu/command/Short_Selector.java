package ccu.command;

import ccu.general.NumberUtils;
import ccu.general.ReadConfig;

public class Short_Selector {

	// essentially converts the 'asdf>=5<=2' bits into their selected things
	private static String getSelector(String selectorGet, String firstOperator, String secondOperator) {
		// all the combinationes of 
		// greaterEqual >=
		// lessEqual <=
		// greaterThan >
		// lessThan <

		String selectorBeg = null;
		String selectorMid = null;
		String selectorEnd = null;
		boolean isScore = true;
		String selectorCalc = null;
		String swapTemp = null;

		// swaps if the order is different
		if (secondOperator.equals("") == false) {
			if (selectorGet.indexOf(firstOperator) > selectorGet.indexOf(secondOperator)) {
				swapTemp = secondOperator + "";
				secondOperator = firstOperator + "";
				firstOperator = swapTemp + "";
			}
		}

		selectorBeg = selectorGet.substring(0, selectorGet.indexOf(firstOperator));

		if (secondOperator.equals("")) {
			selectorMid = selectorGet.substring(selectorGet.indexOf(firstOperator) + firstOperator.length());
			selectorEnd = "0";
		} else {
			selectorMid = selectorGet.substring(selectorGet.indexOf(firstOperator) + firstOperator.length(),
					selectorGet.indexOf(secondOperator));
			selectorEnd = selectorGet.substring(selectorGet.indexOf(secondOperator) + secondOperator.length());
		}

		if (NumberUtils.isInt(selectorMid) == false || NumberUtils.isInt(selectorEnd) == false) {
			isScore = false;
		}

		if (isScore == true) {
			if (firstOperator.equals(">=")) {
				selectorCalc = "score_" + selectorBeg + "_min=" + selectorMid;
			}
			if (firstOperator.equals("<=")) {
				selectorCalc = "score_" + selectorBeg + "=" + selectorMid;
			}
			if (firstOperator.equals(">")) {
				selectorCalc = "score_" + selectorBeg + "_min=" + (Integer.parseInt(selectorMid) + 1);
			}
			if (firstOperator.equals("<")) {
				selectorCalc = "score_" + selectorBeg + "=" + (Integer.parseInt(selectorMid) - 1);
			}

			if (secondOperator.equals(">=")) {
				selectorCalc += ",score_" + selectorBeg + "_min=" + selectorEnd;
			}
			if (secondOperator.equals("<=")) {
				selectorCalc += ",score_" + selectorBeg + "=" + selectorEnd;
			}
			if (secondOperator.equals(">")) {
				selectorCalc += ",score_" + selectorBeg + "_min=" + (Integer.parseInt(selectorEnd) + 1);
			}
			if (secondOperator.equals("<")) {
				selectorCalc += ",score_" + selectorBeg + "=" + (Integer.parseInt(selectorEnd) - 1);
			}

			return selectorCalc;
		} else {

			return selectorGet;
		}

	}

	public static String getCommand(String fullLineGet) {
		String shortcutCalc = null;
		String shortcutEndCalc = null;
		String[] shortcutCalcArray = null;
		String shortcutSelectorCalc = null;
		String[] shortcutSelectorArray = new String[1];
		String shortcutResultCalc = null;
		String shortcutFinalResultCalc = null;
		String selectorBeg = null;
		String selectorEnd = null;
		String getSelectorSave = null;
		String tempRemoveSelector = null;
		boolean greaterEqual = false; // >=
		boolean lessEqual = false; // <=
		boolean greaterThan = false; // >
		boolean lessThan = false; // <
		boolean equalTo = false; // =
		boolean changedLine = false;
		boolean changedFullLine = false;
		boolean isScore = false;

		// @formatter:off
		String[][] gamemodeReplace = {
				{"0", "s", "survival"},
				{"1", "c", "creative"},
				{"2", "a", "adventure"},
				{"3", "sp", "spectator"}
		};
		// @formatter:on

		shortcutCalc = fullLineGet.trim();
		shortcutCalcArray = shortcutCalc.split("@");

		// Essentially anything except the first line will be a possible selector

		changedFullLine = false;
		for (int i = 1; i < shortcutCalcArray.length; i++) {
			changedLine = false;

			// Checks whether it's a proper selector in the first place
			for (String getSelector : ReadConfig.selectorArray) {
				if (("@" + shortcutCalcArray[i].substring(0, 1)).equals(getSelector)) {
					getSelectorSave = getSelector + "";

					// checks whether it has [ and ]
					if (shortcutCalcArray[i].length() >= 2 && shortcutCalcArray[i].substring(1).startsWith("[")
							&& shortcutCalcArray[i].substring(2).contains("]")) {

						// gets the target selector variables inside the square brackets
						shortcutSelectorCalc = shortcutCalcArray[i].substring(2, shortcutCalcArray[i].indexOf("]"));

						// gets everything after the square brackets
						shortcutEndCalc = shortcutCalcArray[i].substring(shortcutCalcArray[i].indexOf("]") + 1);

						// if there are spaces for some reason - invalid
						// If there are curly brackets for some reason - invalid
						if (shortcutSelectorCalc.contains(" ") || shortcutSelectorCalc.contains("{")
								|| shortcutSelectorCalc.contains("}")) {
							break;
						}

						// checks if there are commas (if not, only adds one)
						if (shortcutSelectorCalc.contains(",")) {
							shortcutSelectorArray = shortcutSelectorCalc.split(",");
						} else {
							shortcutSelectorArray = new String[1];
							shortcutSelectorArray[0] = shortcutSelectorCalc;
						}

						// iterates through selector array - this is where the real stuff happens
						for (int j = 0; j < shortcutSelectorArray.length; j++) {

							selectorBeg = null;
							selectorEnd = null;
							tempRemoveSelector = shortcutSelectorArray[j];

							greaterEqual = false; // >=
							lessEqual = false; // <=
							greaterThan = false; // >
							lessThan = false; // <
							equalTo = false; // =

							// Checks >=, <=, >, <, =
							if (tempRemoveSelector.contains(">=")) {
								greaterEqual = true;
								tempRemoveSelector = tempRemoveSelector.replace(">=", "");
							}
							if (tempRemoveSelector.contains("<=")) {
								lessEqual = true;
								tempRemoveSelector = tempRemoveSelector.replace("<=", "");
							}
							if (tempRemoveSelector.contains(">")) {
								greaterThan = true;
								tempRemoveSelector = tempRemoveSelector.replace(">", "");
							}
							if (tempRemoveSelector.contains("<")) {
								lessThan = true;
								tempRemoveSelector = tempRemoveSelector.replace(">", "");
							}
							if (tempRemoveSelector.contains("=")) {
								equalTo = true;
								tempRemoveSelector = tempRemoveSelector.replace("=", "");
							}

							if (equalTo == true) {
								if ((greaterEqual || lessEqual || greaterThan || lessThan) == true) {
									System.out.println("ERROR: Incorrect syntax at '" + shortcutSelectorArray[j] + "' in line '"
											+ fullLineGet + "'");
									System.exit(0);
								} else {
									// meaning '=' makes sense
									isScore = true;
									selectorBeg = shortcutSelectorArray[j].substring(0, shortcutSelectorArray[j].indexOf("="));
									selectorEnd = shortcutSelectorArray[j].substring(shortcutSelectorArray[j].indexOf("=") + 1);

									for (String targetSelector : ReadConfig.targetSelectorArray) {
										if (selectorBeg.equals(targetSelector)) {
											isScore = false;
											
											// if it's either of the first two, sets it to the 3rd
											if (ReadConfig.mcVersion == 4 && selectorBeg.equals("m")) {
												for (String[] checkGamemodeVal : gamemodeReplace) {
													if (selectorEnd.equals(checkGamemodeVal[0])
															|| selectorEnd.equals(checkGamemodeVal[1])) {
														selectorEnd = checkGamemodeVal[2];
													}
												}
												
												shortcutSelectorArray[j] = selectorBeg + "=" + selectorEnd;
												changedLine = true;
											}

											break;
										}
									}

									// if it's already parsed as a score
									if (selectorBeg.startsWith("score_")) {
										isScore = false;
										break;
									}

									// checks if the next one is an int (if not, it isn't a score)
									if (NumberUtils.isInt(selectorEnd) == false) {
										isScore = false;
									}
									// first part is not recognized - meaning it's an objective
									// if it is still a score
									if (isScore == true) {
										shortcutSelectorArray[j] = "score_" + selectorBeg + "=" + selectorEnd + ",score_" + selectorBeg
												+ "_min=" + selectorEnd;
										if (fullLineGet.length() >= 30) {
											// System.out.println(fullLineGet.substring(0, 30));
											// System.out.println(shortcutSelectorArray[j]);
										}

									}
									changedLine = true;
								}
							} else {
								// testing if it's tag=
								if ((greaterEqual || lessEqual || greaterThan || lessThan) == false) {

									// essentially just makes it a tag
									shortcutSelectorArray[j] = "tag=" + shortcutSelectorArray[j];
									changedLine = true;
								} else {
									// all the combinationes of 
									// greaterEqual >=
									// lessEqual <=
									// greaterThan >
									// lessThan <

									if (greaterEqual) {
										// name>=3>5
										if (greaterThan) {
											System.out.println("ERROR: Incorrect syntax at '" + shortcutSelectorArray[j]
													+ "' in line '" + fullLineGet + "'");
											System.exit(0);
										} else {
											// name>=3<=5
											if (lessEqual) {
												shortcutSelectorArray[j] = getSelector(shortcutSelectorArray[j], ">=", "<=");
												changedLine = true;
												continue;
											} else {
												// name>=3<5
												if (lessThan) {
													shortcutSelectorArray[j] = getSelector(shortcutSelectorArray[j], ">=", "<");
													changedLine = true;
													continue;
												} else {
													// name>=3
													shortcutSelectorArray[j] = getSelector(shortcutSelectorArray[j], ">=", "");
													changedLine = true;
													continue;
												}
											}
										}
									}

									if (lessEqual) {
										// name<=3<5
										if (lessThan) {
											System.out.println("ERROR: Incorrect syntax at '" + shortcutSelectorArray[j]
													+ "' in line '" + fullLineGet + "'");
											System.exit(0);
										} else {
											// name<=5>=3
											if (greaterThan) {
												shortcutSelectorArray[j] = getSelector(shortcutSelectorArray[j], "<=", ">");
												changedLine = true;
												continue;
											} else {
												// name<=3
												shortcutSelectorArray[j] = getSelector(shortcutSelectorArray[j], "<=", "");
												changedLine = true;
												continue;
											}
										}
									}

									if (greaterThan) {
										// name>5>=3
										if (lessThan) {
											shortcutSelectorArray[j] = getSelector(shortcutSelectorArray[j], ">", "<");
											changedLine = true;
											continue;
										} else {
											// name>3
											shortcutSelectorArray[j] = getSelector(shortcutSelectorArray[j], ">", "");
											changedLine = true;
											continue;
										}
									}

									if (lessThan) {

										// name<3
										shortcutSelectorArray[j] = getSelector(shortcutSelectorArray[j], "<", "");
										changedLine = true;
										continue;
									}
								}
							}
						}
					}
				}

				// if the selector matches
				if (changedLine == true) {
					changedFullLine = true;
					break;
				}
			}

			// if something changed
			if (changedLine == true) {

				for (int j = 0; j < shortcutSelectorArray.length; j++) {
					if (j == 0) {
						shortcutResultCalc = shortcutSelectorArray[j];
					}
					if (j >= 1 && j - 1 < shortcutSelectorArray.length) {
						shortcutResultCalc += "," + shortcutSelectorArray[j];
					}
					/*if (j == shortcutSelectorArray.length - 1) {
						if (j != 0) {
							shortcutResultCalc += "," + shortcutSelectorArray[j];
						}
					}*/
				}
				shortcutCalcArray[i] = getSelectorSave + "[" + shortcutResultCalc + "]" + shortcutEndCalc;

			} else {
				shortcutCalcArray[i] = "@" + shortcutCalcArray[i];
			}
		}

		if (changedFullLine == true) {
			for (int i = 0; i < shortcutCalcArray.length; i++) {
				if (i == 0) {
					shortcutFinalResultCalc = shortcutCalcArray[i];
				} else {
					shortcutFinalResultCalc += shortcutCalcArray[i];
				}
			}
		}

		/*
		System.out.println(fullLineGet);
		System.out.println(shortcutFinalResultCalc);
		System.out.println("");
		*/

		return shortcutFinalResultCalc;
	}
}
