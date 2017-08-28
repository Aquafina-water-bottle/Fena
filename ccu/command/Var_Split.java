package ccu.command;

import java.util.ArrayList;
import java.util.regex.Pattern;

import ccu.general.ArgUtils;
import ccu.general.NumberUtils;
import ccu.general.StringUtils;

public class Var_Split {
	/** Similar to .split(String) in java
	 * Allows multiple .split arguments
	 * 
	 * Arguments:
	 * GLOBAL / COORDS / TELE because it's an array
	 * 
	 * Always splits into a normal array
	 */

	private ArrayList<String> arraySplit = new ArrayList<String>();

	private int tabNum;
	private String fullLineGet;

	public Var_Split(String fullLineGet, int tabNumGet) {
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {

		Integer arrayType = null;
		Integer visibilityType = null;

		String[] getArrayCalc = null;
		String getArrayName = null;
		String getString = null;

		Integer splitNum = null;

		ArrayList<String> calcSplit = new ArrayList<String>();

		String statementEncase = this.fullLineGet.replaceFirst("SPLIT", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}")) {

			statementEncase = statementEncase.substring(0, statementEncase.length());

			String stringCalc = null;
			int tempCount = 0;

			if (StringUtils.countChars(statementEncase, "{") == StringUtils.countChars(statementEncase, "}")
					&& StringUtils.countChars(statementEncase, "{") > 0) {

				String[] arrayCalc = statementEncase.split(" ");

				for (String line : arrayCalc) {

					if (stringCalc == null) {
						stringCalc = line;
					} else {
						stringCalc += " " + line;
					}

					// counts number of brackets
					tempCount += StringUtils.countChars(line, "{");
					tempCount -= StringUtils.countChars(line, "}");

					if (tempCount == 0) {
						if (stringCalc.equals("{NULL}")) {
							stringCalc = "{}";
						}

						// substring to get rid of curly brackets
						// if it's empty, doesn't add

						if (stringCalc.substring(1, stringCalc.length() - 1).isEmpty()) {
							String tempSave = arraySplit.get(0);
							arraySplit.clear();
							arraySplit.add(tempSave);
							arraySplit.add("");
							break;
						} else {
							arraySplit.add(stringCalc.substring(1, stringCalc.length() - 1));
						}

						stringCalc = null;
					}
				}

			} else {
				System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
				System.exit(0);
			}

			// removes the first element
			String statementArgs = arraySplit.get(0);
			arraySplit.remove(0);

			// makes it split on all if no split char is given
			if (arraySplit.isEmpty()) {
				arraySplit.add("");
			}

			// remvoes ` from split chars
			for (int i = 0; i < arraySplit.size(); i++) {
				arraySplit.set(i, arraySplit.get(i).replace("`", ""));
			}

			if (statementArgs.contains("\t")) {
				System.out.println("ERROR: Arguments in line '" + this.fullLineGet + "' contains unnecessary tab spaces");
				System.exit(0);
			}

			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "GLOBAL":
					visibilityType = 1;
					// removes GLOBAL
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "TEMP":
					visibilityType = 2;
					// removes TEMP
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "RETURN":
					visibilityType = 3;
					// removes RETURN
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "COORDS":
					// removes COORDS
					arrayType = 4;
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "TELE":
					// removes COORDS
					arrayType = 5;
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "MAX":
					// removes MAX
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);

					if (statementArgs.contains(" ") == false) {
						System.out.println("ERROR: Invalid arguments for 'MAX' in line '" + this.fullLineGet + "'");
						System.exit(0);
					}

					String splitNumTest = statementArgs.substring(0, statementArgs.indexOf(" "));
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					if (NumberUtils.isInt(splitNumTest)) {
						splitNum = Integer.parseInt(splitNumTest);
					} else {
						System.out.println("ERROR: 'MAX' in line '" + this.fullLineGet + "' must be proceeded with an integer");
						System.exit(0);
					}
					break;

				}
			}

			// Gets second parameters
			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "GLOBAL":
					if (visibilityType == null) {
						visibilityType = 1;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes GLOBAL
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "TEMP":
					if (visibilityType == null) {
						visibilityType = 2;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes TEMP
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "RETURN":
					if (visibilityType == null) {
						visibilityType = 3;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes RETURN
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "COORDS":
					if (arrayType == null) {
						arrayType = 4;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes COORDS
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "TELE":
					if (arrayType == null) {
						arrayType = 5;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes TELE
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "MAX":
					// removes MAX
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);

					if (statementArgs.contains(" ") == false) {
						System.out.println("ERROR: Invalid arguments for 'MAX' in line '" + this.fullLineGet + "'");
						System.exit(0);
					}

					if (splitNum == null) {
						String splitNumTest = statementArgs.substring(0, statementArgs.indexOf(" "));
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						if (NumberUtils.isInt(splitNumTest)) {
							splitNum = Integer.parseInt(splitNumTest);
						} else {
							System.out.println("ERROR: 'MAX' in line '" + this.fullLineGet + "' must be proceeded with an integer");
							System.exit(0);
						}
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
				}
			}

			// Gets third parameters
			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "GLOBAL":
					if (visibilityType == null) {
						visibilityType = 1;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes GLOBAL
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "TEMP":
					if (visibilityType == null) {
						visibilityType = 2;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes TEMP
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "RETURN":
					if (visibilityType == null) {
						visibilityType = 3;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes RETURN
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "COORDS":
					if (arrayType == null) {
						arrayType = 4;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes COORDS
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "TELE":
					if (arrayType == null) {
						arrayType = 5;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes TELE
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "MAX":
					// removes MAX
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);

					if (statementArgs.contains(" ") == false) {
						System.out.println("ERROR: Invalid arguments for 'MAX' in line '" + this.fullLineGet + "'");
						System.exit(0);
					}

					if (splitNum == null) {
						String splitNumTest = statementArgs.substring(0, statementArgs.indexOf(" "));
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						if (NumberUtils.isInt(splitNumTest)) {
							splitNum = Integer.parseInt(splitNumTest);
						} else {
							System.out.println("ERROR: 'MAX' in line '" + this.fullLineGet + "' must be proceeded with an integer");
							System.exit(0);
						}
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
				}
			}

			// the end should make 'statementArgs' as 'Array_Name' and 'Rest of the string'
			if (statementArgs.contains(" ")) {
				getArrayName = statementArgs.substring(0, statementArgs.indexOf(" "));
				getString = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
			} else {
				getArrayName = statementArgs + "";
				getString = "";
			}

			// Checks if the array name is literally nothing
			if (getArrayName.trim().length() == 0) {
				System.out.println("ERROR: Array name at '" + this.fullLineGet + "' is blank");
				System.exit(0);
			}

			// an array name cannot be anything in the exceptionArray
			for (String checkException : Var_Define.exceptionArray) {
				if (getArrayName.equals(checkException)) {
					System.out.println("ERROR: An array cannot be '" + getArrayName + "' in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
			}

			// Gets options
			if (visibilityType == null) {
				visibilityType = 0;
			}

			if (arrayType == null) {
				arrayType = 1;
			}

			// Gets elements
			int tabNumCalc = this.tabNum; // normal

			switch (visibilityType) {
			case 1: // global
				tabNumCalc = 0;
				break;

			case 2: // temp
				tabNumCalc = this.tabNum + 1;
				break;

			case 3: // return
				tabNumCalc = this.tabNum - 1;
				break;
			}

			// checks for repeats
			int arrayIndex = 0;
			while (arrayIndex < Var_Array.singleArrayNameSave.size()) {
				if (Var_Array.singleArrayNameSave.get(arrayIndex)[2].equals(getArrayName)
						&& Integer.parseInt(Var_Array.singleArrayNameSave.get(arrayIndex)[1]) == tabNumCalc) {

					Var_Array.singleArraySave.remove(arrayIndex);
					Var_Array.singleArrayNameSave.remove(arrayIndex);
				} else {
					arrayIndex++;
				}
			}

			// does the splitting here lol
			calcSplit.add(getString);

			Integer findMinIndex = null;
			Integer splitLength = null;

			int countSplitNum = 0;
			ArrayList<Integer> calcIndexArray = new ArrayList<Integer>();
			
			for (int j = 0; j < calcSplit.size(); j++) {

				calcIndexArray.clear();
				for (int i = 0; i < arraySplit.size(); i++) {
					calcIndexArray.add(StringUtils.indexOfRegex(calcSplit.get(j), "(?<!`)" + Pattern.quote(arraySplit.get(i))));
					if (calcIndexArray.size() >= 1 && calcIndexArray.get(0) != null && calcIndexArray.get(0) == 0
							&& !calcSplit.get(j).isEmpty()) {
						calcIndexArray.set(i, 1);
					}
					// System.out.println(calcIndexArray.size() + "<" + i + " | " + calcIndexArray.get(i) + " | " + calcSplit.get(j));
				}

				if (calcSplit.get(j).isEmpty()) {
					calcSplit.remove(j);
					break;
				}

				findMinIndex = null;
				for (int i = 0; i < calcIndexArray.size(); i++) {
					if (calcIndexArray.get(i) == null) {
						continue;

					} else {
						if (findMinIndex == null) {
							findMinIndex = calcIndexArray.get(i);
						} else {
							findMinIndex = Math.min(findMinIndex, calcIndexArray.get(i));
						}
					}
				}

				if (findMinIndex != null) {
					if (splitNum != null && countSplitNum >= splitNum) {
						break;
					}

					for (int i = 0; i < calcIndexArray.size(); i++) {
						if (calcIndexArray.get(i) == findMinIndex) {
							splitLength = arraySplit.get(i).length();
							break;
						}
					}

					ArrayList<String> tempArray = new ArrayList<String>();
					for (int i = 0; i < calcSplit.size(); i++) {
						if (j == i) {
							tempArray.add(calcSplit.get(j).substring(0, findMinIndex));
							tempArray.add(calcSplit.get(j).substring(findMinIndex + splitLength));
						} else {
							tempArray.add(calcSplit.get(i));
						}
					}

					calcSplit.clear();
					calcSplit.addAll(tempArray);
					countSplitNum++;
				}
			}

			/*
				ArrayList<String> tempSplit = new ArrayList<String>();
				String[] tempSplitCalc = null;
			
				for (int j = 0; j < calcSplit.size(); j++) {
					tempSplitCalc = calcSplit.get(j).split("(?<!`)" + Pattern.quote(arraySplit.get(i)));
			
					for (String splitString : tempSplitCalc) {
						tempSplit.add(splitString);
					}
				}
			
				// re-adds after split
				calcSplit.clear();
				calcSplit.addAll(tempSplit);
			}*/

			// check coords
			for (int i = 0; i < calcSplit.size(); i++) {
				ArgUtils.checkCoords(calcSplit.get(i), arrayType, this.fullLineGet);
			}
			
			getArrayCalc = new String[calcSplit.size()];

			// adds general stuff
			String[] tempArraySave = new String[3];
			tempArraySave[0] = arrayType + "";
			tempArraySave[1] = tabNumCalc + "";
			tempArraySave[2] = getArrayName; // name

			Var_Array.singleArrayNameSave.add(tempArraySave);

			for (int i = 0; i < calcSplit.size(); i++) {
				getArrayCalc[i] = calcSplit.get(i);
			}

			// adds array
			Var_Array.singleArraySave.add(getArrayCalc);

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		return null;
	}
}
