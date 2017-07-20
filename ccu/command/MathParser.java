package ccu.command;

import java.util.ArrayList;

import ccu.general.NumberUtils;
import ccu.general.StringUtils;

class storeValueType {
	public Boolean isDouble = null;
	Long getLong = null;
	Double getDouble = null;
	String getString = null;

	public storeValueType() {
	}

	// Constructor for string apparently
	public storeValueType(String getString) {
		this.getString = getString;
	}

	// Constructor for ints
	public storeValueType(double getNum, Boolean isDouble) {
		this.isDouble = isDouble;
		if (isDouble) {
			this.getDouble = getNum;
		} else {
			this.getLong = (long) getNum;
		}
	}
}

public class MathParser {
	public static String[] getLoopArray(String getArgs, String fullLineGet) {
		/** This gets the full array for arguments like {1 3 + 1}
		 * Eg. The above would return a string array of '1', '2', '3'
		 */
		// Operators are +, -, *, / and ^

		ArrayList<String> calcArray = new ArrayList<String>();
		String[] arrayCalc = null;
		String calcArgs = null;
		int argNum = 0;
		final String[] operatorArray = {"^", "*", "/", "-", "+"};

		// meaning the list is already given and no math is required
		if (getArgs.contains(";")) {
			arrayCalc = getArgs.split(";");
			return arrayCalc;

		} else {
			// if there are no spaces, it would be thought of a singular string
			if (getArgs.contains(" ") == false) {
				arrayCalc = new String[1];
				arrayCalc[0] = getArgs;
				return arrayCalc;
			}

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
			if (arrayCalc[0].equals("")) {
				return null;
			}

			if (arrayCalc.length < 4) {
				// defaults to outputting the string
				arrayCalc = new String[1];
				arrayCalc[0] = getArgs;
				return arrayCalc;
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
									arrayCalc = new String[1];
									arrayCalc[0] = getArgs;
									return arrayCalc;
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
						for (int i = 0; i < arrayCalc.length; i++) {

							// if it's the 3rd element --> detects operator
							if (i == 2) {
								boolean foundOperator = false;
								for (int j = 0; j < operatorArray.length; j++) {
									if (arrayCalc[i].equals(operatorArray[j])) {
										foundOperator = true;
										arrayCalc[i] = j + "";
										break;
									}
								}

								// if the operator wasn't found
								if (foundOperator == false) {
									arrayCalc = new String[1];
									arrayCalc[0] = getArgs;
									return arrayCalc;
								}
								calcArray.add(arrayCalc[i]);

							} else {
								calcArray.add(arrayCalc[i].replace("(", "").replace(")", ""));
							}

						}
					}
				}
			} else { // they don't equal
				System.out.println("ERROR: Unbalanced brackets for LOOP arguments '" + getArgs + "' in line '" + fullLineGet + "'");
				System.exit(0);
			}
		}

		if (calcArray.size() < 4) { // less than 4 arguments = fail
			System.out.println("ERROR: 4 LOOP arguments are required for line '" + fullLineGet + "'");
			System.exit(0);
		}

		ArrayList<String> returnArray = new ArrayList<String>();
		boolean isDouble = false;

		// check if the array contains a double anywhere
		for (String line : calcArray) {
			if (NumberUtils.isNum(line)) {
				if (NumberUtils.isDouble(line)) {
					isDouble = true;
					break;
				}
			} else {
				System.out.println("ERROR: '" + line + "' in line '" + fullLineGet + "' is not a number");
				System.exit(0);
			}
		}

		// calculate calc array for doubles
		if (isDouble) {
			double[] numCalcArray = new double[4];

			for (int i = 0; i < calcArray.size(); i++) {
				numCalcArray[i] = Double.parseDouble(calcArray.get(i));
			}

			double calcNum = numCalcArray[0];
			returnArray.add(NumberUtils.roundDouble(calcNum));

			switch (Integer.parseInt(NumberUtils.roundDoubleToInt(numCalcArray[2]))) {
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
					calcNum = Math.pow(calcNum, numCalcArray[3]);
					if (Double.isNaN(calcNum)) {
						System.out.println("ERROR: Math error resulted in an undefined number in line '" + fullLineGet + "'");
						System.exit(0);
					}
					returnArray.add(NumberUtils.roundDouble(calcNum));

					// detects ending if it equals
					if (Double.parseDouble(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}

				break;

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
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] > 0 && (numCalcArray[3] < 1 && numCalcArray[3] > 0)) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number < ending number and incrementing number > 1 and all negative
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] < 0 && numCalcArray[3] > 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number < 1 and all negative
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[0] < 0 && (numCalcArray[3] < 1 && numCalcArray[3] > 0)) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = calcNum * numCalcArray[3];
					returnArray.add(NumberUtils.roundDouble(calcNum));

					// detects ending if it equals
					if (Double.parseDouble(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}

				break;

			case 2: // /
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

				// if starting number > ending number and incrementing number < 1 and all positive
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[0] > 0 && numCalcArray[3] < 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number < ending number and incrementing number > 1 and all positive
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] > 0 && (numCalcArray[3] > 1 && numCalcArray[3] > 0)) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number < ending number and incrementing number < 1 and all negative
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] < 0 && numCalcArray[3] < 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number > 1 and all negative
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[0] < 0 && (numCalcArray[3] > 1 && numCalcArray[3] > 0)) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = calcNum / numCalcArray[3];
					returnArray.add(NumberUtils.roundDouble(calcNum));

					// detects ending if it equals
					if (Double.parseDouble(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}

				break;

			case 3: // -

				// if starting number < ending number and incrementing number > 0
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[3] > 0) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number < 0
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[3] < 0) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = calcNum - numCalcArray[3];

					returnArray.add(NumberUtils.roundDouble(calcNum));

					// detects ending if it equals
					if (Double.parseDouble(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}
				break;

			case 4: // +

				// if starting number < ending number and incrementing number < 0
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[3] < 0) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number > 0
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[3] > 0) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = calcNum + numCalcArray[3];

					returnArray.add(NumberUtils.roundDouble(calcNum));

					// detects ending if it equals
					if (Double.parseDouble(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Double.parseDouble(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}
				break;
			}

		} else { // calculates int array
			long[] numCalcArray = new long[4];

			for (int i = 0; i < calcArray.size(); i++) {
				numCalcArray[i] = (int) Long.parseLong(calcArray.get(i));
			}

			long calcNum = numCalcArray[0];
			returnArray.add(calcNum + "");

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
					calcNum = (long) Math.pow(calcNum, numCalcArray[3]);
					/*if (Long.isNaN(calcNum)) {
						System.out.println("ERROR: Math error resulted in an undefined number in line '" + fullLineGet + "'");
						System.exit(0);
					}*/
					returnArray.add(calcNum + "");

					// detects ending if it equals
					if (calcNum == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}

				break;

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
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] > 0 && (numCalcArray[3] < 1 && numCalcArray[3] > 0)) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number < ending number and incrementing number > 1 and all negative
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] < 0 && numCalcArray[3] > 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number < 1 and all negative
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[0] < 0 && (numCalcArray[3] < 1 && numCalcArray[3] > 0)) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = calcNum * numCalcArray[3];
					returnArray.add(calcNum + "");

					// detects ending if it equals
					if (calcNum == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}

				break;

			case 2: // /
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

				// if starting number > ending number and incrementing number < 1 and all positive
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[0] > 0 && numCalcArray[3] < 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number < ending number and incrementing number > 1 and all positive
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] > 0 && (numCalcArray[3] > 1 && numCalcArray[3] > 0)) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number < ending number and incrementing number < 1 and all negative
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[0] < 0 && numCalcArray[3] < 1) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number > 1 and all negative
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[0] < 0 && (numCalcArray[3] > 1 && numCalcArray[3] > 0)) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = calcNum / numCalcArray[3];
					returnArray.add(calcNum + "");

					// detects ending if it equals
					if (calcNum == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}

				break;

			case 3: // -

				// if starting number < ending number and incrementing number > 0
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[3] > 0) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number < 0
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[3] < 0) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = calcNum - numCalcArray[3];

					returnArray.add(calcNum + "");

					// detects ending if it equals
					if (calcNum == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}
				break;

			case 4: // +

				// if starting number < ending number and incrementing number < 0
				if (numCalcArray[0] < numCalcArray[1] && numCalcArray[3] < 0) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				// if starting number > ending number and incrementing number > 0
				if (numCalcArray[0] > numCalcArray[1] && numCalcArray[3] > 0) {
					System.out.println("ERROR: LOOP arguments in line '" + fullLineGet + "' are invalid (it cannot reach the ending)");
					System.exit(0);
				}

				while (true) {
					calcNum = calcNum + numCalcArray[3];

					returnArray.add(calcNum + "");

					// detects ending if it equals
					if (calcNum == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Long.parseLong(returnArray.get(returnArray.size() - 1))) == false) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}

					// detects repeat
					if (returnArray.get(returnArray.size() - 1).equals(returnArray.get(returnArray.size() - 2))) {
						returnArray.remove(returnArray.size() - 1);
						break;
					}
				}
				break;
			}
		}

		/*
		System.out.println(calcArray);
		System.out.println(returnArray);
		System.out.println("");
		*/

		String[] returnStringArray = new String[returnArray.size()];
		for (int i = 0; i < returnArray.size(); i++) {
			returnStringArray[i] = returnArray.get(i);
		}

		return returnStringArray;
	}

	public static String getOperation(String getString, String fullLineGet, boolean isStrict, int calcType) {
		/** This is primarily for actual CALC() stuff, including IF
		 */

		// TODO make sin, cos and tan done in this method rather than the calcValue method

		storeValueType getValue = new storeValueType();

		// checks if there are brackets in the first places
		if (StringUtils.countChars(getString, "(") == StringUtils.countChars(getString, ")")) {

			if (StringUtils.countChars(getString, "(") > 0) {

				if ((getString.startsWith("(") && getString.endsWith(")")) == false) {
					getString = "(" + getString + ")";
				}

				String begString = "";
				String midString = "";
				String endString = "";

				int bracketSave = StringUtils.countChars(getString, "(");
				for (int i = 0; i < bracketSave; i++) {
					begString = getString.substring(0, getString.lastIndexOf("("));
					endString = getString.substring(getString.lastIndexOf("("));
					if (endString.contains(")")) {
						midString = endString.substring(0, endString.indexOf(")") + 1);
						endString = endString.substring(endString.indexOf(")") + 1);

						getValue = calcValue(midString.substring(1, midString.length() - 1), fullLineGet, true);

						if (getValue.isDouble) {
							midString = getValue.getDouble + "";
						} else {
							midString = getValue.getLong + "";
						}

						getString = begString + midString + endString;

					} else {
						System.out.println("ERROR: Unbalanced brackets in '" + getString + "' in line '" + fullLineGet + "'");
						System.exit(0);
					}
				}
			} else {
				if (getString.isEmpty()) {
					if (isStrict) {
						System.out.println("ERROR: The argument '" + getString + "' in line '" + fullLineGet + "' is empty");
						System.exit(0);
					}
				} else {
					if (NumberUtils.isNum(getString) == false) {
						getValue = calcValue(getString, fullLineGet, isStrict);
						if (getValue.isDouble == null) {
							if (isStrict) {
								System.out
										.println("ERROR: Arguments in '" + getString + "' in line '" + fullLineGet + "' are invalid");
								System.exit(0);
							}
						} else {
							if (getValue.isDouble) {
								getString = getValue.getDouble + "";

							} else {
								getString = getValue.getLong + "";
							}
						}
					} else {
						if (calcType != 0) {
							getValue = calcValue(getString, fullLineGet, isStrict);
							if (getValue.isDouble == null) {
								if (isStrict == true) {
									System.out.println(
											"ERROR: Arguments in '" + getString + "' in line '" + fullLineGet + "' are invalid");
									System.exit(0);
								}
							} else {
								if (getValue.isDouble) {
									getString = getValue.getDouble + "";

								} else {
									getString = getValue.getLong + "";
								}
							}
						}
					}
				}

				if (getValue.isDouble != null) {
					if (getValue.isDouble) {
						switch (calcType) {
						case 1:
							getValue.getDouble = Math.sin(Math.toRadians(getValue.getDouble));
							break;

						case 2:
							getValue.getDouble = Math.cos(Math.toRadians(getValue.getDouble));
							break;

						case 3:
							getValue.getDouble = Math.tan(Math.toRadians(getValue.getDouble));
							break;
						}

						// turns into long because INT()
						if (calcType == 4) {
							getString = NumberUtils.roundDoubleToInt(getValue.getDouble);

						} else {
							// normal
							getString = NumberUtils.roundDouble(getValue.getDouble) + "";
						}

					} else {
						switch (calcType) {
						case 1:
							getValue.getLong = (long) Math.sin(Math.toRadians(getValue.getLong));
							break;

						case 2:
							getValue.getLong = (long) Math.cos(Math.toRadians(getValue.getLong));
							break;

						case 3:
							getValue.getLong = (long) Math.tan(Math.toRadians(getValue.getLong));
							break;
						}

						// turns into double because DOUBLE()
						if (calcType == 5) {
							getString = NumberUtils.roundDouble(getValue.getLong) + "";
						} else {
							// normal
							getString = getValue.getLong + "";
						}

					}
				}
				return getString;
			}

		} else {
			System.out.println("ERROR: Unbalanced brackets in '" + getString + "' in line '" + fullLineGet + "'");
			System.exit(0);
		}

		if (getValue.isDouble != null) {
			if (getValue.isDouble) {
				switch (calcType) {
				case 1:
					getValue.getDouble = Math.sin(Math.toRadians(getValue.getDouble));
					break;

				case 2:
					getValue.getDouble = Math.cos(Math.toRadians(getValue.getDouble));
					break;

				case 3:
					getValue.getDouble = Math.tan(Math.toRadians(getValue.getDouble));
					break;
				}

				// turns into long because INT()
				if (calcType == 4) {
					getString = NumberUtils.roundDoubleToInt(getValue.getDouble);

				} else {
					// normal
					getString = NumberUtils.roundDouble(getValue.getDouble) + "";
				}

			} else {
				switch (calcType) {
				case 1:
					getValue.getLong = (long) Math.sin(Math.toRadians(getValue.getLong));
					break;

				case 2:
					getValue.getLong = (long) Math.cos(Math.toRadians(getValue.getLong));
					break;

				case 3:
					getValue.getLong = (long) Math.tan(Math.toRadians(getValue.getLong));
					break;
				}

				// turns into double because DOUBLE()
				if (calcType == 5) {
					getString = NumberUtils.roundDouble(getValue.getLong) + "";
				} else {
					// normal
					getString = getValue.getLong + "";
				}
			}
		}

		return getString;
	}

	private static String getLoopOperation(String getString, String fullLineGet, int argNumGet) {
		/** The main difference between the above and this is 'argNumGet'
		 * if that's 3, it detects whether it's a valid loop operator or not (if it isn't, you're a potato)
		 */

		final String[] operatorArray = {"^", "*", "/", "-", "+"};

		// checks if there are brackets in the first places
		if (StringUtils.countChars(getString, "(") == StringUtils.countChars(getString, ")")) {

			if (StringUtils.countChars(getString, "(") > 0) {

				String begString = "";
				String midString = "";
				String endString = "";

				int bracketSave = StringUtils.countChars(getString, "(");
				for (int i = 0; i < bracketSave; i++) {

					// gets last "("
					begString = getString.substring(0, getString.lastIndexOf("("));
					endString = getString.substring(getString.lastIndexOf("("));

					// gets first ")" after "("
					if (endString.contains(")")) {
						midString = endString.substring(0, endString.indexOf(")") + 1);
						endString = endString.substring(endString.indexOf(")") + 1);

						storeValueType getValue = calcValue(midString.substring(1, midString.length() - 1), fullLineGet, true);

						if (getValue.isDouble) {
							midString = getValue.getDouble + "";
						} else {
							midString = getValue.getLong + "";
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
					if (NumberUtils.isNum(getString) == false && argNumGet != 3) {
						System.out.println("ERROR: The argument '" + getString + "' in line '" + fullLineGet + "' is not a number");
						System.exit(0);
					}

					if (NumberUtils.isNum(getString) == false && argNumGet == 3) {
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

	private static storeValueType calcValue(String getString, String fullLineGet, boolean isStrict) {
		// -, +, *, /, ^, %
		// Priority: ^, *, /, %, +, -

		double calcDouble = 0;
		long calcLong = 0;
		String[] arrayCalc = null;

		ArrayList<String> arrayListCalc = new ArrayList<String>();
		ArrayList<Long> arrayLong = new ArrayList<Long>();
		ArrayList<Double> arrayDouble = new ArrayList<Double>();
		ArrayList<Boolean> arrayNumType = new ArrayList<Boolean>();
		ArrayList<Boolean> arrayOperatorType = new ArrayList<Boolean>();

		// final String[] operatorArray = {"^", "*", "/", "%", "+", "-"};
		final String[][] operatorOrderArray = {{"^"}, {"*", "/", "%"}, {"+", "-"}};
		boolean isDouble = false;

		if (NumberUtils.isDouble(getString)) {
			storeValueType returnValue = new storeValueType(Double.parseDouble(getString), true);
			return returnValue;

		} else {
			if (NumberUtils.isInt(getString)) {
				storeValueType returnValue = new storeValueType(Double.parseDouble(getString), false);
				return returnValue;

			} else {

				if (getString.contains(" ") == false) {
					if (isStrict == true) {
						System.out.println("ERROR: Math operations in '" + getString
								+ "' must be separated by spaces (apart from brackets) in line '" + fullLineGet + "'");
						System.exit(0);
					} else {
						storeValueType returnValue = new storeValueType(getString);
						return returnValue;
					}
				} else {
					arrayCalc = getString.split(" ");

					// whether it is a double or int
					for (String line : arrayCalc) {
						arrayListCalc.add(line);

						if (NumberUtils.isDouble(line)) {
							isDouble = true;
						}
					}

					// double overtakes all int
					if (isDouble == true) {
						for (String line : arrayCalc) {

							// adds to arrayNumType only if it's a number
							// adds number to arrayDouble, is null if operator
							if (NumberUtils.isNum(line)) {
								arrayDouble.add(Double.parseDouble(line));
								arrayNumType.add(true);
							} else {
								arrayDouble.add(null);
								arrayNumType.add(false);
							}
						}

					} else { // int
						for (String line : arrayCalc) {

							// adds to arrayNumType only if it's a number
							// adds number to arrayDouble, is null if operator
							if (NumberUtils.isNum(line)) {
								arrayLong.add(Long.parseLong(line));
								arrayNumType.add(true);
							} else {
								arrayLong.add(null);
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

									if (arrayIndex - 1 >= 0 && arrayIndex + 1 < arrayNumType.size() && arrayNumType.get(arrayIndex - 1)
											&& arrayNumType.get(arrayIndex + 1)) {
										switch (arrayListCalc.get(arrayIndex)) {

										case "^":
											if (isDouble) {
												calcDouble = Math.pow(calcDouble = arrayDouble.get(arrayIndex - 1),
														arrayDouble.get(arrayIndex + 1));
												arrayDouble.set(arrayIndex, calcDouble);
											} else {
												calcLong = (long) Math.pow(arrayLong.get(arrayIndex - 1), arrayLong.get(arrayIndex + 1));
												arrayLong.set(arrayIndex, calcLong);
											}
											break;

										case "*":
											if (isDouble) {
												calcDouble = arrayDouble.get(arrayIndex - 1) * arrayDouble.get(arrayIndex + 1);
												arrayDouble.set(arrayIndex, calcDouble);
											} else {
												calcLong = arrayLong.get(arrayIndex - 1) * arrayLong.get(arrayIndex + 1);
												arrayLong.set(arrayIndex, calcLong);
											}
											break;

										case "/":
											if (isDouble) {
												calcDouble = arrayDouble.get(arrayIndex - 1) / arrayDouble.get(arrayIndex + 1);
												arrayDouble.set(arrayIndex, calcDouble);
											} else {
												calcLong = arrayLong.get(arrayIndex - 1) / arrayLong.get(arrayIndex + 1);
												arrayLong.set(arrayIndex, calcLong);
											}
											break;

										case "%":
											if (isDouble) {
												calcDouble = arrayDouble.get(arrayIndex - 1) % arrayDouble.get(arrayIndex + 1);
												arrayDouble.set(arrayIndex, calcDouble);
											} else {
												calcLong = arrayLong.get(arrayIndex - 1) % arrayLong.get(arrayIndex + 1);
												arrayLong.set(arrayIndex, calcLong);
											}
											break;

										case "+":
											if (isDouble) {
												calcDouble = arrayDouble.get(arrayIndex - 1) + arrayDouble.get(arrayIndex + 1);
												arrayDouble.set(arrayIndex, calcDouble);
											} else {
												calcLong = arrayLong.get(arrayIndex - 1) + arrayLong.get(arrayIndex + 1);
												arrayLong.set(arrayIndex, calcLong);
											}
											break;

										case "-":
											if (isDouble) {
												calcDouble = arrayDouble.get(arrayIndex - 1) - arrayDouble.get(arrayIndex + 1);
												arrayDouble.set(arrayIndex, calcDouble);
											} else {
												calcLong = arrayLong.get(arrayIndex - 1) - arrayLong.get(arrayIndex + 1);
												arrayLong.set(arrayIndex, calcLong);
											}
											break;
										}
										
										if (isDouble) {
											arrayDouble.remove(arrayIndex + 1);
											arrayDouble.remove(arrayIndex - 1);
										} else {
											arrayLong.remove(arrayIndex + 1);
											arrayLong.remove(arrayIndex - 1);
										}
										
										arrayNumType.set(arrayIndex, true);
										arrayListCalc.set(arrayIndex, "Num");

										arrayNumType.remove(arrayIndex + 1);
										arrayNumType.remove(arrayIndex - 1);
										arrayListCalc.remove(arrayIndex + 1);
										arrayListCalc.remove(arrayIndex - 1);
										arrayOperatorType.set(arrayIndex, false);
										arrayOperatorType.remove(arrayIndex + 1);
										arrayOperatorType.remove(arrayIndex - 1);

									} else {
										System.out
												.println("ERROR: Operators don't match up with numbers in line '" + fullLineGet + "'");
										System.exit(0);
									}
								}
								arrayIndex++;
							}
						}
					}
				}
			}
		}

		if (isDouble) {
			storeValueType returnValue = new storeValueType(arrayDouble.get(0), true);
			return returnValue;
		} else {
			storeValueType returnValue = new storeValueType(arrayLong.get(0), false);
			return returnValue;
		}
	}

	public static String parseSecondaryStatements(String getString, String fullLineGet) {
		// getCommand is like SIN, COS, TAN, CALC
		// SIN, COS and TAN can be like CALC except the final value returns the sin/cos/tan version

		final String[] secondaryStatementArray = {"SIN", "COS", "TAN", "CALC", "INT", "DOUBLE"};

		// if getStatement is true, then keeps going
		String calcString = null;
		String testBracketString = null;
		String returnString = null;
		boolean getArgs = false;

		String begString = null;
		String endString = null;
		int calcType = 0;

		// gets calcString
		for (String secondaryStatement : secondaryStatementArray) {
			if (getString.contains(secondaryStatement + "(")) {
				begString = getString.substring(0, getString.indexOf(secondaryStatement + "("));
				calcString = getString.substring(getString.indexOf(secondaryStatement + "(") + secondaryStatement.length());

				switch (secondaryStatement) {
				case "CALC":
					calcType = 0;
					break;

				case "SIN":
					calcType = 1;
					break;

				case "COS":
					calcType = 2;
					break;

				case "TAN":
					calcType = 3;
					break;

				case "INT":
					calcType = 4;
					break;

				case "DOUBLE":
					calcType = 5;
					break;
				}

				break;
			}
		}

		// if calcString is not null, then a secondary statement was found
		if (calcString == null) {
			returnString = getString + "";
			return returnString;

		} else {
			// finds brackets
			long bracketNum = StringUtils.countChars(calcString, ")");

			for (int i = 0; i < bracketNum; i++) {
				if (i == 0) {
					testBracketString = calcString.substring(0, calcString.indexOf(")") + 1);
					calcString = calcString.substring(calcString.indexOf(")") + 1);
				} else {
					testBracketString += calcString.substring(0, calcString.indexOf(")") + 1);
					calcString = calcString.substring(calcString.indexOf(")") + 1);
				}

				if (StringUtils.countChars(testBracketString, "(") == StringUtils.countChars(testBracketString, ")")) {
					// success - testBracketString is it
					endString = calcString + "";
					getArgs = true;
					break;
				}
			}

			if (getArgs == false) {
				System.out.println("ERROR: Arguments in '" + getString + "' in line '" + fullLineGet + "' are invalid");
				System.exit(0);
			}

			// no reason with CALC inside any of these
			if (testBracketString.contains("CALC(")) {
				testBracketString = testBracketString.replace("CALC", "");
			}

			// checks if there were any 'SIN', 'COS', 'TAN' - recurring function

			if (testBracketString.contains("SIN") || testBracketString.contains("COS") || testBracketString.contains("TAN")
					|| testBracketString.contains("INT") || testBracketString.contains("DOUBLE")) {
				testBracketString = parseSecondaryStatements(testBracketString, fullLineGet);
			}

			// Sends it to 
			returnString = getOperation(testBracketString, fullLineGet, true, calcType);
		}

		String totalString = begString + returnString + endString;
		for (String secondaryStatement : secondaryStatementArray) {

			if (totalString.contains(secondaryStatement + "(")) {
				totalString = parseSecondaryStatements(totalString, fullLineGet);
			}
		}

		return totalString;
	}
}
