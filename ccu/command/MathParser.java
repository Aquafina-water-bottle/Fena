package ccu.command;

import java.util.ArrayList;

import ccu.general.NumberUtils;
import ccu.general.StringUtils;

public class MathParser {
	public static ArrayList<String> getLoopArray(String getArgs, String fullLineGet) {
		// Operators are +, -, *, / and ^

		ArrayList<String> returnArray = new ArrayList<String>();
		ArrayList<String> calcArray = new ArrayList<String>();
		String[] arrayCalc = null;
		String calcArgs = null;
		final String[] operatorArray = {"+", "-", "*", "/", "^", "%"};
		int argNum = 0;

		// meaning the list is already given and no math is required
		if (getArgs.contains(";")) {
			arrayCalc = getArgs.split(";");
			for (String line : arrayCalc) {
				returnArray.add(line);
			}

			return returnArray;

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
			 * 
			 * 
			 * 
			 * 
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
						for (String line : arrayCalc) {
							calcArray.add(line.replace("(", "").replace(")", ""));
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
								calcArgs = getValue(stringCalc, fullLineGet, argNum); // gets the math stuff here 
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

			// calculate LOOP stuff here
		}

		return calcArray;
	}

	private static String getValue(String getString, String fullLineGet, int argNumGet) {

		// checks if there are brackets in the first places
		if (StringUtils.countChars(getString, "(") == StringUtils.countChars(getString, ")")) {

			if (StringUtils.countChars(getString, "(") > 0) {

				String begString = "";
				String midString = "";
				String endString = "";
				float testFloat = 0;

				for (int i = 0; i < StringUtils.countChars(getString, "("); i++) {
					begString = getString.substring(0, getString.lastIndexOf("("));
					endString = getString.substring(getString.lastIndexOf("("));
					if (endString.contains(")")) {
						midString = endString.substring(0, endString.indexOf(")") + 1);
						endString = endString.substring(endString.indexOf(")") + 1);

						testFloat = calcValue(midString.substring(1, midString.length() - 1), fullLineGet);

						midString = testFloat + "";
						if (midString.contains(".") && Integer.parseInt(midString.substring(midString.indexOf(".") + 1)) == 0) {
							midString = midString.substring(0, midString.indexOf("."));
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

		final String[] operatorArray = {"^", "*", "/", "%", "+", "-"};
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
						if (NumberUtils.isFloat(line)) {
							arrayFloat.add(Float.parseFloat(line));
							arrayNumType.add(true);
						} else {
							arrayFloat.add(null);
							arrayNumType.add(false);
						}
					}

				} else {
					for (String line : arrayCalc) {
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
				for (String operator : operatorArray) {

					arrayIndex = 0;
					while (arrayIndex < arrayListCalc.size()) {
						if (arrayIndex == 0 && arrayNumType.get(arrayIndex) == false) {
							System.out.println(
									"ERROR: The first number in '" + getString + "' in line '" + fullLineGet + "' must be a number");
							System.exit(0);
						}

						if (arrayIndex - 1 == arrayCalc.length && arrayNumType.get(arrayIndex) == false) {
							System.out.println(
									"ERROR: The last number in '" + getString + "' in line '" + fullLineGet + "' must be a number");
							System.exit(0);
						}

						if (arrayListCalc.get(arrayIndex).equals(operator)) {
							if (arrayNumType.get(arrayIndex - 1) && arrayNumType.get(arrayIndex + 1)) {
								switch (operator) {
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

		if (isFloat) {
			return arrayFloat.get(0);
		} else {
			return arrayInt.get(0);
		}
	}
}
