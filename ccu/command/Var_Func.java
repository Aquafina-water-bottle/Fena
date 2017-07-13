package ccu.command;

import java.util.ArrayList;

import ccu.general.ParamUtils;

public class Var_Func {
	/** Used for storing or reusing chunks of commands
	 * Avaliable parameters:
	 * GLOBAL
	 * 
	 * -ARGS is a special FUNC name meant for imported functions
	 * -CCU. is a special prefix to a FUNC or DEF name meant for imported functions
	 * -Is followed by lower camelCase if it's a FUNC and upper CamelCase if it's a DEF
	 * -eg. CCU.Set($RandInt$;3) is a DEF, while CCU.xpNumber is a FUNC
	 * {GLOBAL ACTIVATE CCU.xpNumber args}:
	 * {ACTIVATE CCU.xpNumber args}:
	 * {GLOBAL args}:
	 * {args}:
	 * -ACTIVATE is essentially just putting 'CCU.xpNumber' at the end of the function
	 * 	
	 * How functions should work - No checkCommands() recurring loop
	 * Instead, just copies as is without any modification
	 * Function call without CALL will be modified to add the call and reparsed
	 * 
	 * To check for recurring functions with the combination of definitions and functions-
	 * -does a different constructor for ccuSubSetFile (add another string for function name)
	 * -If at any point a function call matches the function name, error + stop
	 */

	// FUNC array save
	public static ArrayList<String[]> arrayFuncSave = new ArrayList<String[]>();

	// Save param number, tabnum and name
	public static ArrayList<String[]> arrayFuncNameSave = new ArrayList<String[]>();

	// Array calc (removing tab spaces)
	private String[] arrayFuncCalc = null;

	// ArrayList for the activated function
	private ArrayList<String> arrayFuncActivateCalc = new ArrayList<String>();

	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Var_Func(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		// Will not do checkCommands()

		Boolean isGlobal = null;
		Boolean hasActivated = null;
		boolean activateConfirm = false;
		String activatedFunc = null;

		String statementEncase = this.fullLineGet.replaceFirst("FUNC", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {
			String statementArgs = statementEncase.substring(1, statementEncase.length() - 2);

			if (statementArgs.contains("\t")) {
				System.out.println("ERROR: Arguments in line '" + this.fullLineGet + "' contains unnecessary tab spaces");
				System.exit(0);
			}

			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "GLOBAL":
					// removes GLOBAL
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					isGlobal = true;
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

			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "GLOBAL":
					if (isGlobal == null) {
						// removes GLOBAL
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						isGlobal = true;

					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
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

			// sets global settings
			if (isGlobal == null) {
				isGlobal = false;
			}

			// sets activate settings
			if (hasActivated == null) {
				hasActivated = false;
			}

			// checking whether the function name exists
			if (hasActivated == true) {
				for (int i = 0; i < arrayFuncNameSave.size(); i++) {
					if (activatedFunc.equals(arrayFuncNameSave.get(i)[2])) {
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
			}

			// Checks if the function name is literally nothing
			if (statementArgs.trim().length() == 0) {
				System.out.println("ERROR: Function name at '" + this.fullLineGet + "' is blank");
				System.exit(0);
			}

			// a function name cannot be anything in the exceptionArray
			for (String checkException : Var_Define.exceptionArray) {
				if (statementArgs.equals(checkException)) {
					System.out.println("ERROR: A function cannot be '" + statementArgs + "' in line '" + this.fullLineGet + "'");
					System.exit(0);
				}
			}

			// Checks if the function has spaces
			if (statementArgs.trim().contains(" ")) {
				System.out.println("ERROR: Function name at '" + this.fullLineGet + "' contains spaces");
				System.exit(0);
			}

			// Checks whether the defineName and tabnum is the same anywhere --> will remove
			int funcIndex = 0;
			int tabNumCalc = 0;

			// if it's global, tabNumCalc is already set to 1
			if (isGlobal == false) {
				tabNumCalc = this.tabNum - 1;
			}

			// checks for repeats
			while (funcIndex < arrayFuncNameSave.size()) {
				if (arrayFuncNameSave.get(funcIndex)[2].equals(statementArgs)
						&& Integer.parseInt(arrayFuncNameSave.get(funcIndex)[1]) == tabNumCalc) {
					Var_Func.arrayFuncSave.remove(funcIndex);
					Var_Func.arrayFuncNameSave.remove(funcIndex);
				} else {
					funcIndex++;
				}
			}

			// Adds the function to the arrayList while removing tab spaces according to tabNum
			arrayFuncCalc = new String[arrayGet.size()];
			for (int i = 0; i < arrayGet.size(); i++) {
				// Adds full function array while removing tab spaces
				arrayFuncCalc[i] = arrayGet.get(i).substring(this.tabNum);
			}

			String[] addStringArray = new String[3];

			// Gets param number
			addStringArray[0] = ParamUtils.countParams(arrayGet) + "";

			// Adds tab num
			addStringArray[1] = tabNumCalc + "";

			// Adds the name
			addStringArray[2] = statementArgs;

			arrayFuncSave.add(arrayFuncCalc);
			arrayFuncNameSave.add(addStringArray);
		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		if (activateConfirm) {
			return arrayFuncActivateCalc;
		} else {
			return null;
		}
	}
}
