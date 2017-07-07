package ccu.command;

import java.util.ArrayList;

import ccu.general.NumberUtils;
import ccu.general.StringUtils;

public class MathParser {
	public static ArrayList<String> getLoopArray(String getArgs, String fullLineGet) {
		// Operators are +, -, *, / and ^

		ArrayList<String> calcArray = new ArrayList<String>();
		String[] arrayCalc = null;
		String calcArgs = null;
		int argNum = 0;
		final String[] operatorArray = {"^", "*", "/", "-", "+"};

		// meaning the list is already given and no math is required
		if (getArgs.contains(";")) {
			arrayCalc = getArgs.split(";");
			for (String line : arrayCalc) {
				calcArray.add(line);
			}

			return calcArray;

		} else {
			// meaning actual math has to be used lol
			// 1 10 + 1
			// (1 * 4) (12 / 6 - 1) - (0.5 + 0.5)
			// 0.5 2.5 + 0.1
			arrayCalc = getArgs.split(" ");

			/* splits into array
			 * -if open brackets = closed brackets and that there are brackets -->
			 * if there are 4 elements:
			 * 	-remove all brackets because they are unnecessary
			 * 
			 * if there are more than 4 elements
			 * 	-iterates through and count number of brackets until they equal 0, then parse combined string
			 */

			// if arrayCalc has less than 4 arguments --> automatically invalid
			if (arrayCalc.length < 4) {
				System.out.println("ERROR: 4 LOOP arguments are required for line '" + fullLineGet + "'");
				System.exit(0);
			}

			// if bracket numbers equal and that there are brackets
			if (StringUtils.countChars(getArgs, "(") == StringUtils.countChars(getArgs, ")")) {

				if (StringUtils.countChars(getArgs, "(") > 0) {
					// if it's 4
					if (arrayCalc.length == 4) {
						for (int i = 0; i < arrayCalc.length; i++) {

							if (i == 2) {
								boolean foundOperator = false;
								for (int j = 0; j < operatorArray.length; j++) {
									if (arrayCalc[i].equals(operatorArray[j])) {
										foundOperator = true;
										arrayCalc[i] = j + "";
										break;
									}
								}

								if (foundOperator == false) {
									System.out.println("ERROR: The argument '" + arrayCalc[i] + "' in line '" + fullLineGet
											+ "' is not an operator");
									System.exit(0);
								}
							}

							calcArray.add(arrayCalc[i].replace("(", "").replace(")", ""));

						}
					} else {
						// if it's more than 4 --> calculate brackets
						String stringCalc = null;
						int tempCount = 0;

						for (String line : arrayCalc) {

							if (stringCalc == null) {
								stringCalc = line;
							} else {
								stringCalc += " " + line;
							}

							// counts number of brackets
							tempCount += StringUtils.countChars(line, "(");
							tempCount -= StringUtils.countChars(line, ")");

							if (tempCount == 0) {

								argNum++;
								calcArgs = getLoopOperation(stringCalc, fullLineGet, argNum); // gets the math stuff here 
								calcArray.add(calcArgs);

								if (calcArray.size() > 4) {
									System.out.println("ERROR: " + calcArray.size() + " LOOP arguments were found in line '"
											+ fullLineGet + "' (there should be 4)");
									System.exit(0);
								}

								stringCalc = null;
							}
						}
					}
				} else {
					if (arrayCalc.length == 4) {
						for (String line : arrayCalc) {
							calcArray.add(line.replace("(", "").replace(")", ""));
						}
					}
				}
			} else { // they don't equal
				System.out.println("ERROR: Unbalanced brackets for LOOP arguments '" + getArgs + "' in line '" + fullLineGet + "'");
				System.exit(0);
			}
		}

		if (calcArray.size() < 4) {
			System.out.println("ERROR: 4 LOOP arguments are required for line '" + fullLineGet + "'");
			System.exit(0);
		}

		ArrayList<String> returnArray = new ArrayList<String>();
		boolean isFloat = false;

		for (String line : calcArray) {
			boolean isIntCalc = false;

			if (NumberUtils.isInt(line)) {
				isIntCalc = true;
			}
			if (isIntCalc == false && NumberUtils.isFloat(line)) {
				isFloat = true;
				break;
			}
		}

		// calculate calc array
		if (isFloat) {
			float[] numCalcArray = new float[4];

			for (int i = 0; i < calcArray.size(); i++) {
				numCalcArray[i] = Float.parseFloat(calcArray.get(i));
			}

			float calcNum = numCalcArray[0];
			returnArray.add(NumberUtils.roundFloat(calcNum, 9));

			switch (Math.round(numCalcArray[2])) {
			case 0: // ^
				// if starting number > ending number and incrementing number > 1
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[3] > 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number < ending number and incrementing number < 1
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[3] < 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = (float) java.lang.Math.pow(calcNum, numCalcArray[3]);
					if (Float.isNaN(calcNum)) {
						System.out.println("ERROR: Math error resulted in an undefined number in line '" + fullLineGet + "'");
						System.exit(0);
					}
					returnArray.add(NumberUtils.roundFloat(calcNum, 9));

					// detects ending
					if (returnArray.get(returnArray.size() - 1).equals(calcArray.get(1))) {
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}

			case 1: // *
				// if it's incrementing by a negative number
				if (numCalcArray[3] < 0) {
					System.out.println("ERROR: The last loop argument in line '" + fullLineGet + "' cannot be a negative");
					System.exit(0);
				}

				// if the last and first numbers are different signs
				if (NumberUtils.checkSameSign(numCalcArray[0], numCalcArray[1]) == false) {
					System.out.println("ERROR: first two loop arguments in line '" + fullLineGet + "' cannot have different signs");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number > 1 and all positive
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[0] > 0 && numCalcArray[3] > 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number < ending number and incrementing number < 1 and all positive
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] > 0 && numCalcArray[3] < 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number < ending number and incrementing number > 1 and all negative
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] < 0 && numCalcArray[3] > 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number < 1 and all negative
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[0] < 0 && numCalcArray[3] < 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = calcNum * numCalcArray[3];
					returnArray.add(NumberUtils.roundFloat(calcNum, 9));

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Float.parseFloat(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Float.parseFloat(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}

			case 2: // /

			case 3: // -

			case 4: // +

			}

		}

		System.out.println(returnArray);
		return calcArray;
	}

	private static String getLoopOperation(String getString, String fullLineGet, int argNumGet) {

		final String[] operatorArray = {"^", "*", "/", "-", "+"};

		// checks if there are brackets in the first places
		if (StringUtils.countChars(getString, "(") == StringUtils.countChars(getString, ")")) {

			if (StringUtils.countChars(getString, "(") > 0) {

				String begString = "";
				String midString = "";
				String endString = "";
				float testFloat = 0;

				int bracketSave = StringUtils.countChars(getString, "(");
				for (int i = 0; i < bracketSave; i++) {
					begString = getString.substring(0, getString.lastIndexOf("("));
					endString = getString.substring(getString.lastIndexOf("("));
					if (endString.contains(")")) {
						midString = endString.substring(0, endString.indexOf(")") + 1);
						endString = endString.substring(endString.indexOf(")") + 1);

						testFloat = calcValue(midString.substring(1, midString.length() - 1), fullLineGet);

						midString = testFloat + "";
						if (midString.contains(".") && Integer.parseInt(midString.substring(midString.indexOf(".") + 1)) == 0) {
							midString = midString.substring(0, midString.indexOf(".")) + ".0";
							
						} else {
							if (midString.substring(midString.indexOf(".") + 1).length() >= 9) {
								midString = midString.substring(0, midString.indexOf(".") + 9);
							}
						}

						getString = begString + midString + endString;

					} else {
						System.out.println("ERROR: Unbalanced brackets in '" + getString + "' in line '" + fullLineGet + "'");
						System.exit(0);
					}
				}
			} else {
				if (getString.isEmpty()) {
					System.out.println("ERROR: The argument '" + getString + "' in line '" + fullLineGet + "' is empty");
					System.exit(0);
				} else {
					if (NumberUtils.isFloat(getString) == false && argNumGet != 3) {
						System.out.println("ERROR: The argument '" + getString + "' in line '" + fullLineGet + "' is not a number");
						System.exit(0);
					}

					if (NumberUtils.isFloat(getString) == false && argNumGet == 3) {
						boolean foundOperator = false;
						for (int i = 0; i < operatorArray.length; i++) {
							if (getString.equals(operatorArray[i])) {
								foundOperator = true;
								getString = i + "";
								break;
							}
						}

						if (foundOperator == false) {
							System.out.println(
									"ERROR: The argument '" + getString + "' in line '" + fullLineGet + "' is not an operator");
							System.exit(0);
						}
					}
				}

				return getString;
			}

		} else {
			System.out.println("ERROR: Unbalanced brackets in '" + getString + "' in line '" + fullLineGet + "'");
			System.exit(0);
		}

		return getString;
	}

	private static float calcValue(String getString, String fullLineGet) {
		// -, +, *, /, ^, %
		// Priority: ^, *, /, %, +, -

		float calcFloat = 0;
		int calcInt = 0;
		String[] arrayCalc = null;

		ArrayList<String> arrayListCalc = new ArrayList<String>();
		ArrayList<Integer> arrayInt = new ArrayList<Integer>();
		ArrayList<Float> arrayFloat = new ArrayList<Float>();
		ArrayList<Boolean> arrayNumType = new ArrayList<Boolean>();
		ArrayList<Boolean> arrayOperatorType = new ArrayList<Boolean>();

		// final String[] operatorArray = {"^", "*", "/", "%", "+", "-"};
		final String[][] operatorOrderArray = {{"^"}, {"*", "/", "%"}, {"+", "-"}};
		boolean isInt = false;
		boolean isFloat = false;

		if (NumberUtils.isFloat(getString)) {
			return Float.parseFloat(getString);
		} else {
			if (getString.contains(" ") == false) {
				System.out.println("ERROR: Math operations in '" + getString
						+ "'must be seperated by spaces (apart from brackets) in line'" + fullLineGet + "'");
				System.exit(0);
			} else {
				arrayCalc = getString.split(" ");

				// whether it is a float or int
				for (String line : arrayCalc) {
					arrayListCalc.add(line);
					if (NumberUtils.isInt(line)) {
						isInt = true;
					}
					if (isInt == false && NumberUtils.isFloat(line)) {
						isFloat = true;
					}
				}

				// float overtakes all int
				if (isFloat == true) {
					for (String line : arrayCalc) {

						// adds to arrayNumType only if it's a number
						// adds number to arrayFloat, is null if operator
						if (NumberUtils.isFloat(line)) {
							arrayFloat.add(Float.parseFloat(line));
							arrayNumType.add(true);
						} else {
							arrayFloat.add(null);
							arrayNumType.add(false);
						}
					}

				} else { // int
					for (String line : arrayCalc) {

						// adds to arrayNumType only if it's a number
						// adds number to arrayFloat, is null if operator
						if (NumberUtils.isInt(line)) {
							arrayInt.add(Integer.parseInt(line));
							arrayNumType.add(true);
						} else {
							arrayInt.add(null);
							arrayNumType.add(false);
						}
					}

				}

				int arrayIndex = 0;
				for (String[] operatorArray : operatorOrderArray) {
					arrayOperatorType.clear();
					for (int i = 0; i < arrayNumType.size(); i++) {
						boolean foundOperator = false;
						for (String operator : operatorArray) {
							if (arrayNumType.get(i) == false && arrayListCalc.get(i).equals(operator)) {
								foundOperator = true;
								break;
							}
						}

						if (foundOperator == true) {
							arrayOperatorType.add(true);
						} else {
							arrayOperatorType.add(false);
						}
					}

					for (int i = 0; i < arrayOperatorType.size(); i++) {
						arrayIndex = 0;
						while (arrayIndex < arrayListCalc.size()) {
							if (arrayIndex == 0 && arrayNumType.get(arrayIndex) == false) {
								System.out.println("ERROR: The first number in '" + getString + "' in line '" + fullLineGet
										+ "' must be a number");
								System.exit(0);
							}

							if (arrayIndex - 1 == arrayCalc.length && arrayNumType.get(arrayIndex) == false) {
								System.out.println("ERROR: The last number in '" + getString + "' in line '" + fullLineGet
										+ "' must be a number");
								System.exit(0);
							}

							if (arrayOperatorType.get(arrayIndex) == true) {
								if (arrayNumType.get(arrayIndex - 1) && arrayNumType.get(arrayIndex + 1)) {
									switch (arrayListCalc.get(arrayIndex)) {

									case "^":
										if (isFloat) {
											calcFloat = (float) java.lang.Math.pow(calcFloat = arrayFloat.get(arrayIndex - 1),
													arrayFloat.get(arrayIndex + 1));
											arrayFloat.set(arrayIndex, calcFloat);
										} else {
											calcInt = (int) java.lang.Math.pow(arrayInt.get(arrayIndex - 1),
													arrayInt.get(arrayIndex + 1));
											arrayInt.set(arrayIndex, calcInt);
										}
										break;

									case "*":
										if (isFloat) {
											calcFloat = arrayFloat.get(arrayIndex - 1) * arrayFloat.get(arrayIndex + 1);
											arrayFloat.set(arrayIndex, calcFloat);
										} else {
											calcInt = arrayInt.get(arrayIndex - 1) * arrayInt.get(arrayIndex + 1);
											arrayInt.set(arrayIndex, calcInt);
										}
										break;

									case "/":
										if (isFloat) {
											calcFloat = arrayFloat.get(arrayIndex - 1) / arrayFloat.get(arrayIndex + 1);
											arrayFloat.set(arrayIndex, calcFloat);
										} else {
											calcInt = arrayInt.get(arrayIndex - 1) / arrayInt.get(arrayIndex + 1);
											arrayInt.set(arrayIndex, calcInt);
										}
										break;

									case "%":
										if (isFloat) {
											calcFloat = arrayFloat.get(arrayIndex - 1) % arrayFloat.get(arrayIndex + 1);
											arrayFloat.set(arrayIndex, calcFloat);
										} else {
											calcInt = arrayInt.get(arrayIndex - 1) % arrayInt.get(arrayIndex + 1);
											arrayInt.set(arrayIndex, calcInt);
										}
										break;

									case "+":
										if (isFloat) {
											calcFloat = arrayFloat.get(arrayIndex - 1) + arrayFloat.get(arrayIndex + 1);
											arrayFloat.set(arrayIndex, calcFloat);
										} else {
											calcInt = arrayInt.get(arrayIndex - 1) + arrayInt.get(arrayIndex + 1);
											arrayInt.set(arrayIndex, calcInt);
										}
										break;

									case "-":
										if (isFloat) {
											calcFloat = arrayFloat.get(arrayIndex - 1) - arrayFloat.get(arrayIndex + 1);
											arrayFloat.set(arrayIndex, calcFloat);
										} else {
											calcInt = arrayInt.get(arrayIndex - 1) - arrayInt.get(arrayIndex + 1);
											arrayInt.set(arrayIndex, calcInt);
										}
										break;
									}

									if (isFloat) {
										arrayFloat.remove(arrayIndex + 1);
										arrayFloat.remove(arrayIndex - 1);
									} else {
										arrayInt.remove(arrayIndex + 1);
										arrayInt.remove(arrayIndex - 1);
									}

									arrayNumType.set(arrayIndex, true);
									arrayListCalc.set(arrayIndex, "Num");

									arrayNumType.remove(arrayIndex + 1);
									arrayNumType.remove(arrayIndex - 1);
									arrayListCalc.remove(arrayIndex + 1);
									arrayListCalc.remove(arrayIndex - 1);

								} else {
									System.out.println("ERROR: Operators don't match up with numbers in line '" + fullLineGet + "'");
									System.exit(0);
								}
							}
							arrayIndex++;
						}
					}
				}
			}
		}

		if (isFloat) {
			return arrayFloat.get(0);
		} else {
			return arrayInt.get(0);
		}
	}
}
