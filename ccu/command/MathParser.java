package ccu.command;

import java.util.ArrayList;

import ccu.general.NumberUtils;
import ccu.general.StringUtils;

class storeValueType {
	public Boolean isFloat = null;
	Integer getInt = null;
	Float getFloat = null;
	String getString = null;

	// Constructor for string apparently
	public storeValueType(String getString) {
		this.getString = getString;
	}

	// Constructor for ints
	public storeValueType(float getNum, Boolean isFloat) {
		this.isFloat = isFloat;
		if (isFloat) {
			this.getFloat = getNum;
		} else {
			this.getInt = (int) getNum;
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
									System.out.println("ERROR: The argument '" + arrayCalc[i] + "' in line '" + fullLineGet
											+ "' is not an operator");
									System.exit(0);
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
		boolean isFloat = false;

		// check if the array contains a float anywhere
		for (String line : calcArray) {
			if (NumberUtils.isNum(line)) {
				if (NumberUtils.isFloat(line)) {
					isFloat = true;
					break;
				}
			} else {
				System.out.println("ERROR: '" + line + "' in line '" + fullLineGet + "' is not a number");
				System.exit(0);
			}
		}

		// calculate calc array for floats
		if (isFloat) {
			float[] numCalcArray = new float[4];

			for (int i = 0; i < calcArray.size(); i++) {
				numCalcArray[i] = Float.parseFloat(calcArray.get(i));
			}

			float calcNum = numCalcArray[0];
			returnArray.add(NumberUtils.roundFloat(calcNum));

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
					if (Double.isNaN(calcNum)) {
						System.out.println("ERROR: Math error resulted in an undefined number in line '" + fullLineGet + "'");
						System.exit(0);
					}
					returnArray.add(NumberUtils.roundFloat(calcNum));

					// detects ending if it equals
					if (Float.parseFloat(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

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
					returnArray.add(NumberUtils.roundFloat(calcNum));

					// detects ending if it equals
					if (Float.parseFloat(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

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
					returnArray.add(NumberUtils.roundFloat(calcNum));

					// detects ending if it equals
					if (Float.parseFloat(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

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

					returnArray.add(NumberUtils.roundFloat(calcNum));

					// detects ending if it equals
					if (Float.parseFloat(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

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

					returnArray.add(NumberUtils.roundFloat(calcNum));

					// detects ending if it equals
					if (Float.parseFloat(returnArray.get(returnArray.size() - 1)) == numCalcArray[1]) {
						break;
					}

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
				break;
			}

		} else { // calculates int array
			int[] numCalcArray = new int[4];

			for (int i = 0; i < calcArray.size(); i++) {
				numCalcArray[i] = Integer.parseInt(calcArray.get(i));
			}

			int calcNum = numCalcArray[0];
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
					calcNum = (int) java.lang.Math.pow(calcNum, numCalcArray[3]);
					/*if (Integer.isNaN(calcNum)) {
						System.out.println("ERROR: Math error resulted in an undefined number in line '" + fullLineGet + "'");
						System.exit(0);
					}*/
					returnArray.add(calcNum + "");

					// detects ending if it equals
					if (calcNum == numCalcArray[1]) {
						break;
					}

					// detects ending by checking whether finalNum - previous and finalNum - current are different signs
					if (NumberUtils.checkSameSign(numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 1))) == false) {
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
					if (NumberUtils.checkSameSign(numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 1))) == false) {
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
					if (NumberUtils.checkSameSign(numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 1))) == false) {
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
					if (NumberUtils.checkSameSign(numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 1))) == false) {
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
					if (NumberUtils.checkSameSign(numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 2)),
							numCalcArray[1] - Integer.parseInt(returnArray.get(returnArray.size() - 1))) == false) {
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

	public static String getOperation(String getString, String fullLineGet, boolean isStrict) {
		/** This is primarily for actual CALC() stuff, including IF
		 */

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

						storeValueType getValue = calcValue(midString.substring(1, midString.length() - 1), fullLineGet, true);

						if (getValue.isFloat) {
							midString = getValue.getFloat + "";
						} else {
							midString = getValue.getInt + "";
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
					if (NumberUtils.isNum(getString) == false) {
						storeValueType getValue = calcValue(getString, fullLineGet, isStrict);
						if (getValue.isFloat == null) {
							if (isStrict == true) {
								System.out
										.println("ERROR: Arguments in '" + getString + "' in line '" + fullLineGet + "' are invalid");
								System.exit(0);
							}
						} else {
							if (getValue.isFloat) {
								getString = getValue.getFloat + "";
							} else {
								getString = getValue.getInt + "";
							}
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

						if (getValue.isFloat) {
							midString = getValue.getFloat + "";
						} else {
							midString = getValue.getInt + "";
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
		boolean isFloat = false;

		if (NumberUtils.isFloat(getString)) {
			storeValueType returnValue = new storeValueType(Float.parseFloat(getString), true);
			return returnValue;

		} else {
			if (NumberUtils.isInt(getString)) {
				storeValueType returnValue = new storeValueType(Float.parseFloat(getString), false);
				return returnValue;

			} else {

				if (getString.contains(" ") == false) {
					if (isStrict == true) {
						System.out.println("ERROR: Math operations in '" + getString
								+ "' must be separated by spaces (apart from brackets) in line'" + fullLineGet + "'");
						System.exit(0);
					} else {
						storeValueType returnValue = new storeValueType(getString);
						return returnValue;
					}
				} else {
					arrayCalc = getString.split(" ");

					// whether it is a float or int
					for (String line : arrayCalc) {
						arrayListCalc.add(line);

						if (NumberUtils.isFloat(line)) {
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

		if (isFloat) {
			storeValueType returnValue = new storeValueType(arrayFloat.get(0), true);
			return returnValue;
		} else {
			storeValueType returnValue = new storeValueType(arrayInt.get(0), false);
			return returnValue;
		}
	}

	public static String parseSecondaryStatements(String getString) {
		// getCommand is like SIN, COS, TAN, CALC
		// SIN, COS and TAN can be like CALC except the final value returns the sin/cos/tan version
		
		final String[] secondaryStatementArray = {"SIN", "COS", "TAN", "CALC"};

		// if getStatement is true, then keeps going
		String calcString = null;
		String testBracketString = null;
		String returnString = null;

		// gets calcString
		for (String secondaryStatement : secondaryStatementArray) {
			if (getString.contains(secondaryStatement + "(")) {
				calcString = getString.substring(getString.lastIndexOf(secondaryStatement + "("));
				System.out.println(calcString + " " + secondaryStatement);
				break;
			}
		}
		
		// if calcString is not null, then a secondary statement was found
		if (calcString == null) {
			returnString = getString + "";
			return returnString;
		} else {
			// finds brackets
			for (int i = 0; i < StringUtils.countChars(calcString, ")"); i++) {
				if (i == 0) {
					calcString = calcString.substring(0, calcString.indexOf(")"));
				} else {
					
				}
			}
			
			
		}

		return getString;
	}
}
