package ccu.command;

import java.util.ArrayList;

import ccu.general.ArgUtils;
import ccu.general.ParamUtils;

public class Var_Call {
	public static ArrayList<String> checkFunction = new ArrayList<String>();

	private ArrayList<String> arrayReturn = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Var_Call(String fullLineGet, int tabNumGet) {
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {

		/** It's the exact same as stating a function name
		 * It just allows you to call multiple functions in the same line
		 * USAGE:
		 * 
		 * CALL {Func_asdf;Func_AyyLmao}
		 */

		String statementArgs = "";
		boolean functionExists = false;
		String getParamCalc = null;
		ArrayList<String> useParamsCalc = new ArrayList<String>();
		String lineCalc = null;
		int funcIndexSave = 0;

		// Checking tab spaces
		String whitespaceCalc = ArgUtils.checkWhiteSpace(this.fullLineGet, this.tabNum);
		String statementEncase = this.fullLineGet.replaceFirst("CALL", "").replaceAll("^\\s+", "");

		// if it's a proper CALL
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}")) {
			statementArgs = statementEncase.substring(1, statementEncase.length() - 1);

			// if it contains multiple functions - returns normal func names in seperate lines
			if (statementArgs.contains(",")) {
				String[] statementArgsArray = statementArgs.split(",");
				for (int i = 0; i < statementArgsArray.length; i++) {
					arrayReturn.add(whitespaceCalc + "CALL {" + statementArgsArray[i].trim() + "}");
				}
			} else {
				// check for params
				if (statementArgs.contains("(") && statementArgs.endsWith(")")
						&& statementArgs.indexOf("(") < statementArgs.indexOf(")")) {
					getParamCalc = statementArgs.substring(statementArgs.indexOf("("));
					statementArgs = statementArgs.substring(0, statementArgs.indexOf("("));
				}

				// checks if it has spaces
				if (statementArgs.contains(" ") || statementArgs.contains("\t")) {
					System.out
							.println("ERROR: Function '" + statementArgs + "' in line '" + this.fullLineGet + "' cannot have spaces");
					System.exit(0);
				}

				// does the actual thing
				for (int funcIndex = Var_Func.arrayFuncNameSave.size() - 1; funcIndex >= 0; funcIndex--) {

					// if it matches
					if (statementArgs.equals(Var_Func.arrayFuncNameSave.get(funcIndex)[2])) {

						useParamsCalc = ParamUtils.getParams(getParamCalc,
								Integer.parseInt(Var_Func.arrayFuncNameSave.get(funcIndex)[0]));
						
						for (int i = 0; i < Var_Func.arrayFuncSave.get(funcIndex).length; i++) {
							lineCalc = whitespaceCalc + Var_Func.arrayFuncSave.get(funcIndex)[i];
							arrayReturn.add(lineCalc);
						}

						functionExists = true;
						funcIndexSave = funcIndex;
						break;
					}
				}

				if (functionExists == false) {
					System.out.println("ERROR: Function '" + statementArgs + "' in line '" + this.fullLineGet + "' does not exist");
					System.exit(0);
				}

				// checks duplicates in checkFunction
				checkFunction.add(statementArgs);

				for (int i = 0; i < checkFunction.size(); i++) {
					for (int j = 0; j < checkFunction.size(); j++) {
						if (checkFunction.get(i).equals(checkFunction.get(j)) && i != j) {
							System.out.println(
									"ERROR: Recurring function '" + checkFunction.get(i) + "' at line '" + this.fullLineGet + "'");
							System.exit(0);
						}
					}
				}

				// replaces params
				this.arrayReturn = ParamUtils.replaceParams(this.arrayReturn, useParamsCalc,
						Integer.parseInt(Var_Func.arrayFuncNameSave.get(funcIndexSave)[0]), tabNum);

				ArgUtils.checkCommands(this.arrayReturn, tabNum);
				checkFunction.clear();
			}

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		return this.arrayReturn;
	}

	public String getFuncCall() {
		String statementEncase = this.fullLineGet.replaceFirst("CALL", "").replaceAll("^\\s+", "");

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

		return whitespaceCalc + "CALL {" + statementEncase + "}";
	}

}
