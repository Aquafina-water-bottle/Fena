package ccu.command;

import java.util.ArrayList;
import java.util.regex.Pattern;

import ccu.general.ArgUtils;
import ccu.general.NumberUtils;

public class Var_Set {
	/** Allows setting a certain element of an array to a string
	 * 
	 * Arguments:
	 * GLOBAL
	 * 
	 * Always splits into a normal array
	 * 
	 * Eg. SET GLOBAL Arr_Name[3][2] Something
	 */

	private int tabNum;
	private String fullLineGet;

	public Var_Set(String fullLineGet, int tabNumGet) {
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		boolean isGlobal = false;
		boolean is2D = false;

		String statementEncase = this.fullLineGet.replaceFirst("SET", "").replaceAll("^\\s+", "");
		String statementArgs = statementEncase.substring(0, statementEncase.length());
		String getArrayName = null;
		String getString = null;
		String indexTest = null;
		int index1 = 0;
		int index2 = 0;
		Integer indexSave = null;

		if (statementArgs.contains("\t")) {
			System.out.println("ERROR: Arguments in line '" + this.fullLineGet + "' contains unnecessary tab spaces");
			System.exit(0);
		}

		if (statementArgs.contains(" ")) {
			switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
			case "GLOBAL":
				isGlobal = true;
				// removes GLOBAL
				statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
				break;
			}

			// the end should make 'statementArgs' as 'Array_Name' and 'Rest of the string'
			if (statementArgs.contains(" ")) {
				getArrayName = statementArgs.substring(0, statementArgs.indexOf(" "));
				getString = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
			} else {
				System.out.println("ERROR: Line '" + this.fullLineGet + "' does not have enough arguments");
				System.exit(0);
			}

			// Checks if the array name is literally nothing
			if (getArrayName.trim().length() == 0) {
				System.out.println("ERROR: Array name at '" + this.fullLineGet + "' is blank");
				System.exit(0);
			}

			// Gets parameters
			if (getArrayName.contains("[") && getArrayName.contains("]") && getArrayName.indexOf("[") < getArrayName.indexOf("]")) {
				indexTest = getArrayName.substring(getArrayName.indexOf("[") + 1, getArrayName.indexOf("]"));
				getArrayName = getArrayName.replaceFirst(Pattern.quote("[" + indexTest + "]"), "");
				if (NumberUtils.isInt(indexTest)) {
					index1 = Integer.parseInt(indexTest);
				} else {
					System.out.println("ERROR: Array parameters in line '" + this.fullLineGet + "' is not an integer");
					System.exit(0);
				}

				if (getArrayName.contains("[") && getArrayName.contains("]")
						&& getArrayName.indexOf("[") < getArrayName.indexOf("]")) {
					indexTest = getArrayName.substring(getArrayName.indexOf("[") + 1, getArrayName.indexOf("]"));
					getArrayName = getArrayName.replaceFirst(Pattern.quote("[" + indexTest + "]"), "");
					if (NumberUtils.isInt(indexTest)) {
						index2 = Integer.parseInt(indexTest);
						is2D = true;
					} else {
						System.out.println("ERROR: Array parameters in line '" + this.fullLineGet + "' is not an integer");
						System.exit(0);
					}
				}

			} else {
				System.out.println("ERROR: Array parameters in line '" + this.fullLineGet + "' are required");
				System.exit(0);
			}

			// attempts to find the array
			int tabNumCalc = 0;
			if (isGlobal == false) {
				tabNumCalc = tabNum;
			}

			if (is2D) {
				for (int i = Var_Array.doubleArrayNameSave.size() - 1; i >= 0; i--) {
					if (tabNumCalc == 0) {
						if (Var_Array.doubleArrayNameSave.get(i)[2].equals(getArrayName)
								&& Integer.parseInt(Var_Array.doubleArrayNameSave.get(i)[1]) == tabNumCalc) {
							indexSave = i + 0;
							break;
						}

					} else {
						if (Var_Array.doubleArrayNameSave.get(i)[2].equals(getArrayName)
								&& Integer.parseInt(Var_Array.doubleArrayNameSave.get(i)[1]) <= tabNumCalc) {
							indexSave = i + 0;
							break;
						}
					}
				}

			} else {
				for (int i = 0; i < Var_Array.singleArrayNameSave.size(); i++) {
					if (tabNumCalc == 0) {
						if (Var_Array.singleArrayNameSave.get(i)[2].equals(getArrayName)
								&& Integer.parseInt(Var_Array.singleArrayNameSave.get(i)[1]) == tabNumCalc) {
							indexSave = i + 0;
							break;
						}

					} else {
						if (Var_Array.singleArrayNameSave.get(i)[2].equals(getArrayName)
								&& Integer.parseInt(Var_Array.singleArrayNameSave.get(i)[1]) <= tabNumCalc) {
							indexSave = i + 0;
							break;
						}
					}
				}
			}

			if (indexSave == null) {
				System.out.println("ERROR: Array '" + getArrayName + "' in line '" + this.fullLineGet + "' could not be found");
				System.exit(0);
			}

			if (is2D) {

				// checks whether the indexes actually work
				if (Var_Array.doubleArraySave.get(indexSave).length > index1
						&& Var_Array.doubleArraySave.get(indexSave)[index1].length > index2) {
					Var_Array.doubleArraySave.get(indexSave)[index1][index2] = getString;
					ArgUtils.checkCoords(getString, Integer.parseInt(Var_Array.doubleArrayNameSave.get(indexSave)[0]),
							this.fullLineGet);
				} else {
					System.out.println(
							"ERROR: Array parameters for '" + getArrayName + "' in line '" + this.fullLineGet + "' are invalid");
					System.exit(0);
				}

			} else {
				// checks whether the indexes actually work
				if (Var_Array.singleArraySave.get(indexSave).length > index1) {
					Var_Array.singleArraySave.get(indexSave)[index1] = getString;
					ArgUtils.checkCoords(getString, Integer.parseInt(Var_Array.singleArrayNameSave.get(indexSave)[0]),
							this.fullLineGet);
				} else {
					System.out.println(
							"ERROR: Array parameters for '" + getArrayName + "' in line '" + this.fullLineGet + "' are invalid");
					System.exit(0);
				}

			}

			// an array name cannot be anything in the exceptionArray
			for (String checkException : Var_Define.exceptionArray) {
				if (getArrayName.equals(checkException)) {
					System.out.println("ERROR: An array cannot be '" + getArrayName + "' in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
			}

			/*
			// check coords
			for (int i = 0; i < calcSplit.size(); i++) {
				ArgUtils.checkCoords(calcSplit.get(i), arrayType, this.fullLineGet);
			}
			
			// adds array
			Var_Array.singleArraySave.add(getArrayCalc);
			*/

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		return null;
	}
}
