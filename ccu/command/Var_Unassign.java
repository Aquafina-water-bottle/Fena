package ccu.command;

import java.util.ArrayList;

public class Var_Unassign {
	/** Used to remove any variable types
	 * Parameters:
	 * GLOBAL
	 * ARRAY, DEF, FUNC, OBJLIST, TEAMLIST
	 * 
	 * Usage:
	 * UNASSIGN {GLOBAL ARRAY Arr_Name}
	 * (Type must be specified)
	 */

	private int tabNum;
	private String fullLineGet;

	public Var_Unassign(String fullLineGet, int tabNumGet) {
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		Boolean isGlobal = null;
		Integer unassignType = null;

		// Checks for whitespace
		String whitespaceCalc = this.fullLineGet.substring(0,
				(this.fullLineGet.length() - this.fullLineGet.replaceAll("^\\s+", "").length()));
		if (whitespaceCalc.contains(" ")) {
			System.out.println("ERROR: Line '" + this.fullLineGet + "' contains spaces instead of tab spaces");
			System.exit(0);
		}

		// Checks for actual spaces instead of tab spaces
		if (whitespaceCalc.length() - whitespaceCalc.replace("\t", "").length() != this.tabNum) {
			System.out.println("ERROR: Line '" + this.fullLineGet + "' contains an incorrect number of tab spaces");
			System.exit(0);
		}

		String statementEncase = this.fullLineGet.replaceFirst("UNASSIGN", "").replaceAll("^\\s+", "");

		// if it's a proper UNASSIGN
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}")) {
			String statementArgs = statementEncase.substring(1, statementEncase.length() - 1);

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

				case "ARRAY":
					unassignType = 1;
					// removes ARRAY
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "DEF":
					unassignType = 2;
					// removes DEF
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "FUNC":
					unassignType = 3;
					// removes FUNC
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "OBJLIST":
					unassignType = 4;
					// removes OBJLIST
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "TEAMLIST":
					unassignType = 5;
					// removes TEAMLIST
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;
				}
			}

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
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "ARRAY":
					if (unassignType == null) {
						unassignType = 1;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes ARRAY
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "DEF":
					if (unassignType == null) {
						unassignType = 2;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes DEF
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "FUNC":
					if (unassignType == null) {
						unassignType = 3;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes FUNC
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "OBJLIST":
					if (unassignType == null) {
						unassignType = 4;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes OBJLIST
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "TEAMLIST":
					if (unassignType == null) {
						unassignType = 5;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					// removes TEAMLIST
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;
				}
			}

			if (isGlobal == null) {
				isGlobal = false;
			}

			if (isGlobal == true) {
				tabNum = 0;
			}

			if (unassignType == null) {
				System.out.println("ERROR: Unassign type is not specified in line '" + this.fullLineGet + "'");
				System.exit(0);
			}
			
			if (unassignType == 2) {
				int defIndex = Var_Define.arrayDefineSave.size() - 1;
				while (defIndex >= 0) {
					if (Var_Define.arrayDefineSave.get(defIndex)[2].equals(statementArgs)) {
						if (isGlobal == true && Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[1]) == tabNum) {
							Var_Define.arrayDefineSave.remove(defIndex);
							break;
						} else {
							if (Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[1]) <= tabNum) {
								Var_Define.arrayDefineSave.remove(defIndex);
								break;
							}
							defIndex--;
						}
					} else {
						defIndex--;
					}
				}
			}
			
			if (unassignType == 3) {
				int funcIndex = Var_Func.arrayFuncNameSave.size() - 1;
				while (funcIndex >= 0) {
					if (Var_Func.arrayFuncNameSave.get(funcIndex).equals(statementArgs)) {
						if (isGlobal == true && Var_Func.arrayFuncTabNumSave.get(funcIndex) == tabNum) {
							Var_Func.arrayFuncSave.remove(funcIndex);
							Var_Func.arrayFuncNameSave.remove(funcIndex);
							Var_Func.arrayFuncTabNumSave.remove(funcIndex);
							Var_Func.arrayFuncParamSave.remove(funcIndex);
							break;
						} else {
							if (Var_Func.arrayFuncTabNumSave.get(funcIndex) <= tabNum) {
								Var_Func.arrayFuncSave.remove(funcIndex);
								Var_Func.arrayFuncNameSave.remove(funcIndex);
								Var_Func.arrayFuncTabNumSave.remove(funcIndex);
								Var_Func.arrayFuncParamSave.remove(funcIndex);
								break;
							}
							funcIndex--;
						}
					} else {
						funcIndex--;
					}
				}
			}

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		return null;
	}
}
