package ccu.command;

import java.util.ArrayList;

import ccu.general.ArgUtils;
import ccu.general.StringUtils;

public class Var_Array {
	/** Array stuff
	 * Arguments:
	 * GLOBAL can be added to affect all and not just within the encapsulation
	 * COORDS --> set of 3 or 6 numbers
	 * TELE --> set of 5 numbers
	 * ACTIVATE (Name) --> Literally the exact same as the function one 
	 * 
	 * if :
	 * ARRAY {GLOBAL Arr_Name}:
	 * 		element1
	 * 		element2
	 * 		element3
	 * 
	 * then:
	 * Arr_Name[S] will return 'element1;element2;element3'
	 * Arr_Name[L] will return '2'
	 * 
	 * they are meant to be used in LOOP
	 * 
	 * LOOP {Arr_Name[S]}:
	 * 		say |0|
	 * 
	 * will return:
	 * say element1
	 * say element2
	 * say element3
	 * 
	 * 2D arrays can be made using
	 * ARRAY {Arr_Rand}:
	 * 		{
	 * 			say asdf
	 * 			say asdf2
	 * 		} {
	 * 			say asdf_1
	 * 			say asdf_2
	 * 		}
	 * 
	 */

	// 2D array save
	public static ArrayList<String[][]> doubleArraySave = new ArrayList<String[][]>();
	public static ArrayList<String[]> doubleArrayNameSave = new ArrayList<String[]>();

	// Normal array save
	public static ArrayList<String[]> singleArraySave = new ArrayList<String[]>();
	public static ArrayList<String[]> singleArrayNameSave = new ArrayList<String[]>();

	// Get ACTIVATE func
	private ArrayList<String> arrayFuncActivateCalc = new ArrayList<String>();

	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Var_Array(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {

		boolean is2DArray = false;
		Integer arrayType = null;
		Boolean isGlobal = null;

		Boolean hasActivated = null;
		String activatedFunc = null;

		String[] getArrayCalc = null;
		String[][] get2DArrayCalc = null;

		String statementEncase = this.fullLineGet.replaceFirst("ARRAY", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {
			String statementArgs = statementEncase.substring(1, statementEncase.length() - 2);
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

				case "ACTIVATE":
					// removes ACTIVATE
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					hasActivated = true;

					if (statementArgs.contains(" ") == false) {
						System.out.println("ERROR: Invalid arguments for 'ACTIVATE' in line '" + this.fullLineGet + "'");
						System.exit(0);
					}

					activatedFunc = statementArgs.substring(0, statementArgs.indexOf(" "));

					// testing if it has parameters and does not have an ending bracket
					while (true) {
						if (activatedFunc.contains("(") && activatedFunc.endsWith(")") == false) {
							if (statementArgs.contains(" ")) {

								// removes current
								statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
								activatedFunc += " " + statementArgs.substring(0, statementArgs.indexOf(" "));
								
							} else {
								System.out.println("ERROR: Invalid arguments for 'ACTIVATE' in line '" + this.fullLineGet + "'");
								System.exit(0);
							}
						} else {
							break;
						}
					}
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;
				}
			}

			// Gets second parameters
			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "GLOBAL":
					if (isGlobal == null) {
						isGlobal = true;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes GLOBAL
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

				case "ACTIVATE":
					if (hasActivated == null) {
						// removes ACTIVATE
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						hasActivated = true;

						if (statementArgs.contains(" ") == false) {
							System.out.println("ERROR: Invalid arguments for 'ACTIVATE' in line '" + this.fullLineGet + "'");
							System.exit(0);
						}

						activatedFunc = statementArgs.substring(0, statementArgs.indexOf(" "));

						// testing if it has parameters and does not have an ending bracket
						while (true) {
							if (activatedFunc.contains("(") && activatedFunc.endsWith(")") == false) {
								if (statementArgs.contains(" ")) {

									// removes current
									statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
									activatedFunc += " " + statementArgs.substring(0, statementArgs.indexOf(" "));
								} else {
									System.out.println("ERROR: Invalid arguments for 'ACTIVATE' in line '" + this.fullLineGet + "'");
									System.exit(0);
								}
							} else {
								break;
							}
						}

						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);

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
					if (isGlobal == null) {
						isGlobal = true;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes GLOBAL
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

				case "ACTIVATE":
					if (hasActivated == null) {
						// removes ACTIVATE
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						hasActivated = true;

						if (statementArgs.contains(" ") == false) {
							System.out.println("ERROR: Invalid arguments for 'ACTIVATE' in line '" + this.fullLineGet + "'");
							System.exit(0);
						}

						activatedFunc = statementArgs.substring(0, statementArgs.indexOf(" "));

						// testing if it has parameters and does not have an ending bracket
						while (true) {
							if (activatedFunc.contains("(") && activatedFunc.endsWith(")") == false) {
								if (statementArgs.contains(" ")) {

									// removes current
									statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
									activatedFunc += " " + statementArgs.substring(0, statementArgs.indexOf(" "));
								} else {
									System.out.println("ERROR: Invalid arguments for 'ACTIVATE' in line '" + this.fullLineGet + "'");
									System.exit(0);
								}
							} else {
								break;
							}
						}

						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);

					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
				}
			}

			// the end should make 'statementArgs' as the actual use thing (Array name)
			
			/*
			// sets activate settings
			if (hasActivated == null) {
				hasActivated = false;
			}

			// checking whether the function name exists
			
			if (hasActivated == true) {
				for (int i = 0; i < Var_Func.arrayFuncNameSave.size(); i++) {
					if (activatedFunc.equals(Var_Func.arrayFuncNameSave.get(i)[2])) {
						activateConfirm = true;
						break;
					}
				}

				if (activateConfirm) {
					arrayFuncActivateCalc.add(this.fullLineGet.substring(0, this.tabNum - 1) + activatedFunc);
				} else {
					System.out.println("ERROR: Function '" + activatedFunc + "' in line '" + this.fullLineGet + "'does not exist");
					System.exit(0);
				}
			}*/

			String whiteSpaceCalc = this.fullLineGet.substring(0, this.tabNum - 1);

			// Checks if the array name is literally nothing
			if (statementArgs.trim().length() == 0) {
				System.out.println("ERROR: Array name at '" + this.fullLineGet + "' is blank");
				System.exit(0);
			}

			// an array name cannot be anything in the exceptionArray
			for (String checkException : Var_Define.exceptionArray) {
				if (statementArgs.equals(checkException)) {
					System.out.println("ERROR: An array cannot be '" + statementArgs + "' in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
			}

			// Checks if the array has spaces
			if (statementArgs.trim().contains(" ")) {
				System.out.println("ERROR: Array name at '" + this.fullLineGet + "' contains spaces");
				System.exit(0);
			}

			// Gets options
			if (isGlobal == null) {
				isGlobal = false;
			}

			if (arrayType == null) {
				arrayType = 1;
			}

			// Gets elements
			/* is2DArray is set to true if
			 * first element is '{'and last element is '}'
			 * first and last element have whiteSpaceCalc + 1 tab spaces 
			 * second element has whiteSpaceCalc + 2 tab spaces 
			 */

			if (this.arrayGet.size() >= 3 && this.arrayGet.get(0).trim().equals("{")
					&& this.arrayGet.get(this.arrayGet.size() - 1).trim().equals("}")
					&& StringUtils.countChars(this.arrayGet.get(0), "\t") == whiteSpaceCalc.length() + 1
					&& StringUtils.countChars(this.arrayGet.get(1), "\t") == whiteSpaceCalc.length() + 2
					&& StringUtils.countChars(this.arrayGet.get(this.arrayGet.size() - 1), "\t") == whiteSpaceCalc.length() + 1) {
				is2DArray = true;
			}

			int tabNumCalc = 0;

			if (isGlobal == false) {
				tabNumCalc = this.tabNum - 1;
			}

			// checks for repeats
			int arrayIndex = 0;
			if (is2DArray) {
				while (arrayIndex < doubleArrayNameSave.size()) {
					if (doubleArrayNameSave.get(arrayIndex)[2].equals(statementArgs)
							&& Integer.parseInt(doubleArrayNameSave.get(arrayIndex)[1]) == tabNumCalc) {
						Var_Array.doubleArraySave.remove(arrayIndex);
						Var_Array.doubleArrayNameSave.remove(arrayIndex);
					} else {
						arrayIndex++;
					}
				}
			} else {
				while (arrayIndex < singleArrayNameSave.size()) {
					if (singleArrayNameSave.get(arrayIndex)[2].equals(statementArgs)
							&& Integer.parseInt(singleArrayNameSave.get(arrayIndex)[1]) == tabNumCalc) {
						Var_Array.singleArraySave.remove(arrayIndex);
						Var_Array.singleArrayNameSave.remove(arrayIndex);
					} else {
						arrayIndex++;
					}
				}
			}

			if (is2DArray) { // splits whenever '} {' is found
				ArgUtils.checkWhiteSpace(this.arrayGet, tabNum, true);

				ArrayList<String> tempArray = new ArrayList<String>();
				ArrayList<String[]> tempArrayStorage = new ArrayList<String[]>();

				for (int i = 1; i < arrayGet.size(); i++) {

					// split
					if (StringUtils.countChars(arrayGet.get(i), "\t") == whiteSpaceCalc.length() + 1
							&& arrayGet.get(i).trim().equals("} {")) {

						// creates string array
						tempArray = ArgUtils.checkCommands(tempArray, tabNum + 1);

						getArrayCalc = new String[tempArray.size()];
						for (int j = 0; j < tempArray.size(); j++) {
							getArrayCalc[j] = tempArray.get(j).trim();
							if (getArrayCalc[j].equals("NULL")) {
								getArrayCalc[j] = "";
							}
							ArgUtils.checkCoords(getArrayCalc[j], arrayType, this.fullLineGet);
						}

						tempArrayStorage.add(getArrayCalc);
						tempArray.clear();
						continue;
					}

					// end
					if (arrayGet.size() - 1 == i) {

						// creates string array
						tempArray = ArgUtils.checkCommands(tempArray, tabNum + 1);
						getArrayCalc = new String[tempArray.size()];
						
						for (int j = 0; j < tempArray.size(); j++) {
							getArrayCalc[j] = tempArray.get(j).trim();
							if (getArrayCalc[j].equals("NULL")) {
								getArrayCalc[j] = "";
							}
							ArgUtils.checkCoords(getArrayCalc[j], arrayType, this.fullLineGet);
						}

						tempArrayStorage.add(getArrayCalc);
					}

					tempArray.add(arrayGet.get(i));
				}

				get2DArrayCalc = new String[tempArrayStorage.size()][];

				// adds general stuff
				String[] tempArraySave = new String[3];
				tempArraySave[0] = arrayType + "";
				tempArraySave[1] = tabNumCalc + "";
				tempArraySave[2] = statementArgs; // name
				doubleArrayNameSave.add(tempArraySave);

				// adds array
				for (int i = 0; i < tempArrayStorage.size(); i++) {
					get2DArrayCalc[i] = tempArrayStorage.get(i);
				}
				doubleArraySave.add(get2DArrayCalc);

			} else { // easy part here- just convert everything into String[]
				ArgUtils.checkWhiteSpace(this.arrayGet, tabNum, false);
				arrayGet = ArgUtils.checkCommands(arrayGet, tabNum);

				getArrayCalc = new String[arrayGet.size()];

				// adds general stuff
				String[] tempArraySave = new String[3];
				tempArraySave[0] = arrayType + "";
				tempArraySave[1] = tabNumCalc + "";
				tempArraySave[2] = statementArgs; // name
				singleArrayNameSave.add(tempArraySave);

				for (int i = 0; i < arrayGet.size(); i++) {
					getArrayCalc[i] = arrayGet.get(i).trim();
				}

				// adds array
				singleArraySave.add(getArrayCalc);
			}

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		/*
		for (String[][] asdf : doubleArraySave) {
			for (String[] asdf2 : asdf) {
				for (String asdf3 : asdf2) {
					System.out.print(asdf3 + " | ");
				}
				System.out.println("");
			}
			System.out.println("");
		}
		*/

		/*
		for (String[] asdf : singleArraySave) {
			for (String asdf2 : asdf) {
				System.out.println(asdf2);
			}
			System.out.println("");
		}
		*/

		if (hasActivated != null && hasActivated) {
			arrayFuncActivateCalc.add(this.fullLineGet.substring(0, this.tabNum - 1) + activatedFunc);
			return arrayFuncActivateCalc;
		} else {
			return null;
		}
	}

}
