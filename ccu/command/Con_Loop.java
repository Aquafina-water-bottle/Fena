package ccu.command;

import java.util.ArrayList;

import ccu.general.ArgUtils;
import ccu.general.NumberUtils;
import ccu.general.ParamUtils;
import ccu.general.StringUtils;

public class Con_Loop {
	private ArrayList<String> arrayLoopReturn = new ArrayList<String>();
	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Con_Loop(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		
		/** Iterates though either an array or a given set of numbers
		 * Valid operators are: +, -, /, *, ^, () (NOTICE: % is not valid)
		 * Examples:
		 * {1 3 + 1} --> (1, 2, 3)
		 * {(3 3 * 2)} --> (3)
		 * {ArR_Asdf[L]} --> Length of an array from 0 to length - 1
		 * {2 64 ^ 2} --> (2, 4, 16, 64)
		 * {2 64 * 2} --> (2, 4, 8, 16, 32, 64)
		 */
		// System.out.println("LINE " + fullLineGet);

		ArrayList<String[]> loopArrayStorage = new ArrayList<String[]>();
		ArrayList<String> paramArrayGet = new ArrayList<String>();
		int paramNum = 0;
		int loopNum = 0;

		// Removes "LOOP" and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("LOOP", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {

			statementEncase = statementEncase.substring(0, statementEncase.length() - 1).replace("CALC(","(");
			// Gets rid of the last colon
			// splits in spaces, gets number of {}

			// if it's 4

			// if it's more than 4 --> calculate brackets
			String stringCalc = null;
			int tempCount = 0;

			if (StringUtils.countChars(statementEncase, "{") == StringUtils.countChars(statementEncase, "}")
					&& StringUtils.countChars(statementEncase, "{") > 0) {

				String[] arrayCalc = statementEncase.split(" ");
				String[] loopArray = null;

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
						loopArray = MathParser.getLoopArray(stringCalc.substring(1, stringCalc.length() - 1), fullLineGet); // gets the math stuff here
						loopArrayStorage.add(loopArray);
						stringCalc = null;
					}
				}

				// checks tab spaces
				ArgUtils.checkWhiteSpace(this.arrayGet, this.tabNum, false);
				
				for (int i = 0; i < this.arrayGet.size(); i++) {
					// removes a tab space infront of the line
					this.arrayGet.set(i, this.arrayGet.get(i).substring(1));
				}

				// gets param num within the encapsulated array
				paramNum = ParamUtils.countParams(arrayGet, this.fullLineGet);

				// makes sure it loops through all arrays
				loopNum = NumberUtils.getMaxSize(loopArrayStorage);
				for (int i = 0; i < loopNum; i++) {

					// get params from the specific index (if n/a, returns "")
					paramArrayGet = ParamUtils.getLoopParams(loopArrayStorage, i, paramNum);

					// replaces params and adds it onto the arrayLoopReturn
					arrayLoopReturn.addAll(ParamUtils.replaceParams(this.arrayGet, paramArrayGet, paramNum, tabNum - 1));
					
				}
				ArgUtils.checkCommands(arrayLoopReturn, tabNum - 1);

			} else {
				System.out.println("ERROR: Curly brackets in line '" + this.fullLineGet + "' are not balanced");
				System.out.println(arrayGet);
				System.exit(0);
			}

			/*
			System.out.println("");
			for (String[] asdf : loopArrayStorage) {
				for (String asdf2 : asdf) {
					System.out.print(asdf2 + "\t");
				}
				System.out.println("");
			}
			*/

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}
		
		return arrayLoopReturn;
	}
}
