package ccu.command;

import java.util.ArrayList;

import ccu.general.NumberUtils;
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
	 * {PARSESEP Func_Something}
	 * {GLOBAL ACTIVATE CCU.xpNumber ARGS}:
	 * {ACTIVATE CCU.xpNumber ARGS}:
	 * {GLOBAL ARGS}:
	 * {ARGS}:
	 * -ACTIVATE is essentially just putting 'CCU.xpNumber' at the end of the function
	 * -PARSESEP is to separate variables from each other by adding a tab space to them
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

		Integer visibilityType = null;
		Boolean hasActivated = null;
		Boolean parseSep = null;
		String activatedFunc = null;
		Integer splitNum = null;

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
					visibilityType = 1;
					break;
					
				case "TEMP":
					// removes TEMP
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					visibilityType = 2;
					break;
					
				case "RETURN":
					// removes TEMP
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					visibilityType = 3;
					break;
					
				case "PARSESEP":
					// removes PARSESEP
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					parseSep = true;
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
					if (visibilityType == null) {
						// removes GLOBAL
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						visibilityType = 1;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
					
				case "TEMP":
					if (visibilityType == null) {
						// removes TEMP
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						visibilityType = 2;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
					
				case "RETURN":
					if (visibilityType == null) {
						// removes TEMP
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						visibilityType = 3;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
					
				case "PARSESEP":
					if (parseSep == null) {
						// removes GLOBAL
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						parseSep = true;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
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
			
			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "GLOBAL":
					if (visibilityType == null) {
						// removes GLOBAL
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						visibilityType = 1;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
					
				case "TEMP":
					if (visibilityType == null) {
						// removes TEMP
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						visibilityType = 2;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
					
				case "RETURN":
					if (visibilityType == null) {
						// removes TEMP
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						visibilityType = 3;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
					
				case "PARSESEP":
					if (parseSep == null) {
						// removes GLOBAL
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						parseSep = true;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
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

			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "GLOBAL":
					if (visibilityType == null) {
						// removes GLOBAL
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						visibilityType = 1;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
					
				case "TEMP":
					if (visibilityType == null) {
						// removes TEMP
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						visibilityType = 2;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
					
				case "RETURN":
					if (visibilityType == null) {
						// removes TEMP
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						visibilityType = 3;
						
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;
					
				case "PARSESEP":
					if (parseSep == null) {
						// removes GLOBAL
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
						parseSep = true;

					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
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
			// sets split num settings
			if (splitNum == null) {
				splitNum = -1;
			}
			
			// sets global settings
			if (visibilityType == null) {
				visibilityType = 0;
			}

			// sets activate settings
			if (hasActivated == null) {
				hasActivated = false;
			}

			// checking whether the function name exists
			/*
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
			}*/
			
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

			if (parseSep == null) {
				parseSep = false;
			}

			// Checks whether the defineName and tabnum is the same anywhere --> will remove
			int funcIndex = 0;
			int tabNumCalc = this.tabNum - 1;
			
			switch (visibilityType) {
			case 1:
				tabNumCalc = 0;
				break;
				
			case 2:
				tabNumCalc = this.tabNum;
				break;
				
			case 3:
				tabNumCalc = this.tabNum - 2;
				break;
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

			String[] addStringArray = new String[5];

			// Gets param number
			addStringArray[0] = ParamUtils.countParams(arrayGet, this.fullLineGet) + "";

			// Adds tab num
			addStringArray[1] = tabNumCalc + "";
			
			// Adds the name
			addStringArray[2] = statementArgs;

			// Adds whether it parses vars or not
			addStringArray[3] = parseSep + "";
			
			// Adds max split num
			addStringArray[4] = splitNum + "";

			arrayFuncSave.add(arrayFuncCalc);
			arrayFuncNameSave.add(addStringArray);
		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		if (hasActivated != null && hasActivated) {
			arrayFuncActivateCalc.add(this.fullLineGet.substring(0, this.tabNum - 1) + activatedFunc);
			return arrayFuncActivateCalc;
		} else {
			return null;
		}
	}
	
	public static void garbageCollect(int tabNum, int resetlastFunc) {
		boolean resetIndexCalc = false;

		// reset all functions that don't work with the decreasing tab numbers
		for (int funcIndex = 0; funcIndex < arrayFuncNameSave.size(); funcIndex++) {
			if ((resetlastFunc <= 1) && funcIndex == arrayFuncNameSave.size() - 1) {
				break;
			}
			if (resetIndexCalc == true) {
				resetIndexCalc = false;
				funcIndex = 0;
			}
			if (tabNum <= Integer.parseInt(arrayFuncNameSave.get(funcIndex)[1])) {
				resetIndexCalc = true;
				arrayFuncSave.remove(funcIndex);
				arrayFuncNameSave.remove(funcIndex);
			}
		}
	}
}
