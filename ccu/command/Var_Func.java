package ccu.command;

import java.util.ArrayList;

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
	 * eg.
	 * FUNC {GLOBAL CCU.xpNumber}:
	 * 		ayy
	 * 		lmao
	 * 		args
	 * 		using the arguments really well here
	 * 
	 * 
	 * FUNC {args ACTVATE CCU.xpNumber}
	 * 		the
	 * 		actual
	 * 		arguments
	 * 
	 * the above FUNC is saved and CCU.xpNumber is called as a function call
	 * 
	 * 
	 * 
	 * How functions should work - No checkCommands() recurring loop
	 * Instead, just copies as is without any modification
	 * if there is a function call, it will check for params and whether it is isolated in a singular line
	 * then pastes in replacement of the line (aka returns function array) --> it should automatically do resetArray
	 * 
	 * To check for recurring functions with the combination of definitions and functions-
	 * -does a different constructor for ccuSubSetFile (add another string for function name)
	 * -If at any point a function call matches the function name, error + stop
	 * 
	 * FUNC {GLOBAL Func_Lmao}:
	 * 		say |0|
	 * 		FUNC GLOBAL {Func_Asdf}:
	 * 			say |0|
	 * 			say |0;1| first, |0| second
	 * 		Func_Asdf(3)
	 * Func_Lmao(1)
	 * Func_Asdf(5)
	 * 
	 * turns into
	 * 
	 * say |0|
	 * FUNC GLOBAL {Func_Asdf}:
	 * 		say |0|
	 * 		say |0;1| first, |0| second
	 * Func_Asdf(3)
	 * Func_Asdf(5)
	 * 
	 * turns into
	 * 
	 * say |0|
	 * say 3
	 * say |0| first, 3 second
	 * say 5
	 * say |0| first, 5 second
	 * 
	 * 
	 * turns into
	 * 
	 * say 1
	 * say 3
	 * say 1 first, 3 second
	 * say 5
	 * say 1 first, 5 second
	 */

	// FUNC array save
	public static ArrayList<String[]> arrayFuncSave = new ArrayList<String[]>();

	// Save FUNC name
	public static ArrayList<String> arrayFuncNameSave = new ArrayList<String>();

	// Save tabNum per func
	public static ArrayList<Integer> arrayFuncTabNumSave = new ArrayList<Integer>();

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
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					isGlobal = true;
					break;

				case "ACTIVATE":
					// removes ACTIVATE
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					hasActivated = true;

					if (statementArgs.contains(" ") == false) {
						System.out.println("ERROR: Invalid arguments for 'ACTIVATE' in line '" + this.fullLineGet + "'");
						System.exit(0);
					}

					activatedFunc = statementArgs.substring(0, statementArgs.indexOf(" "));
					break;
				}
			}

			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "GLOBAL":
					if (isGlobal == null) {
						// removes GLOBAL
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
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
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
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
									statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
									activatedFunc += " " + statementArgs.substring(0, statementArgs.indexOf(" "));
								} else {
									System.out.println("ERROR: Invalid arguments for 'ACTIVATE' in line '" + this.fullLineGet + "'");
									System.exit(0);
								}
							} else {
								break;
							}
						}

						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());

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

			if (isGlobal == true) {
				this.tabNum = 0;
			}

			// sets activate settings
			if (hasActivated == null) {
				hasActivated = false;
			}

			// checking whether the function name exists
			if (hasActivated == true) {
				for (String getFuncName : arrayFuncNameSave) {
					if (activatedFunc.equals(getFuncName)) {
						activateConfirm = true;
						break;
					}
				}

				if (activateConfirm == false) {
					System.out.println("ERROR: Function '" + activatedFunc + "' in line '" + this.fullLineGet + "'does not exist");
					System.exit(0);
				} else {
					arrayFuncActivateCalc.add(this.fullLineGet.substring(0, this.tabNum - 1) + activatedFunc);
				}
			}

			// Adds full function array
			arrayFuncCalc = new String[arrayGet.size()];
			for (int i = 0; i < arrayGet.size(); i++) {
				arrayFuncCalc[i] = arrayGet.get(i).substring(this.tabNum);
			}

			arrayFuncSave.add(arrayFuncCalc);

			// Adds the name
			arrayFuncNameSave.add(statementArgs);

			// Adds tab num
			arrayFuncTabNumSave.add(this.tabNum);
		}

		if (activateConfirm) {
			return arrayFuncActivateCalc;
		} else {
			return null;
		}
	}
}
