package ccu.command;

import java.util.ArrayList;

import ccu.general.ArgUtils;
import ccu.general.StringUtils;

public class Con_Cond {
	private ArrayList<String> arrayCondReturn = new ArrayList<String>();
	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Con_Cond(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		/**
		 * This mostly just gets the name in the curly brackets, checks for more
		 * statements, and then puts the commands in an array and returns null
		 */
		// System.out.println("LINE " + fullLineGet);

		ArgUtils.checkCommands(this.arrayGet, tabNum);
		
		ArgUtils.checkWhiteSpace(this.arrayGet, tabNum, false);

		// Removes "COND " and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("COND", "").replaceAll("^\\s+", "");
		if (statementEncase.endsWith(":")) {

			for (int i = 0; i < this.arrayGet.size(); i++) {
				// Adds "CCU_COND_" in front of each command assuming it isn't already in the front
				String newString = null;

				// checks tab spaces
				String whiteSpaceCalc = StringUtils.getWhiteSpace(this.arrayGet.get(i));

				if (this.arrayGet.get(i).replaceAll("^\\s+", "").contains("CCU_COND_")) {
					newString = this.arrayGet.get(i).replace("CCU_COND_", "");
					newString = whiteSpaceCalc.substring(1) + "CCU_COND_" + newString.replace(whiteSpaceCalc, "");
				} else {
					// Puts CCU_COND_ before the thing
					newString = whiteSpaceCalc.substring(1) + "CCU_COND_" + this.arrayGet.get(i).replace(whiteSpaceCalc, "");
				}
				arrayCondReturn.add(newString);
			}

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		return arrayCondReturn;
	}
}
