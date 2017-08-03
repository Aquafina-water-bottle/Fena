package ccu.command;

import java.util.ArrayList;

import ccu.general.ArgUtils;

public class Con_Else {
	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;
	private Boolean parseArray;

	public Con_Else(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet, Boolean parseArray) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
		this.parseArray = parseArray;
	}

	public ArrayList<String> getArray() {
		/** ELSE is just as it seems lol
		 */

		ArrayList<String> returnArray = new ArrayList<String>();

		// Removes "COND " and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("ELSE", "").replaceAll("^\\s+", "");
		if (statementEncase.endsWith(":")) {

			// meaning it's invalid
			if (parseArray == null) {
				System.out.println("ERROR: Line '" + this.fullLineGet + "' is invalid as it is not preceeded by 'IF' or 'ELIF'.");
				System.exit(0);
			}

			if (parseArray == true) {
				ArgUtils.checkWhiteSpace(this.arrayGet, tabNum, false);
				ArgUtils.checkCommands(this.arrayGet, tabNum);
				
				for (String getLine : this.arrayGet) {
					returnArray.add(getLine.substring(1));
				}
			} else {
				returnArray = null;
			}

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		return returnArray;
	}
}
