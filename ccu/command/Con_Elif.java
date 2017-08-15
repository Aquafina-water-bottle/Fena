package ccu.command;

import java.util.ArrayList;

public class Con_Elif {
	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;
	private Boolean parseArray;

	public Con_Elif(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet, Boolean parseArray) {
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
		String statementEncase = this.fullLineGet.replaceFirst("ELIF", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {

			// meaning it's invalid
			if (parseArray == null) {
				System.out.println("ERROR: Line '" + this.fullLineGet + "' is invalid as it is not preceeded by 'IF' or 'ELIF'.");
				System.exit(0);
			}
			
			// goes to if right after because elif is like that
			if (parseArray == true) {
				
				// checkcommands and checking lines are done here
				Con_If objIf = new Con_If(this.arrayGet, this.tabNum, this.fullLineGet, false);
				returnArray = objIf.getArray();
				
			} else {
				returnArray.add(this.fullLineGet.substring(0, tabNum - 1) + "CCU_ReturnTrue");
				return returnArray;
			}

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		return returnArray;
	}
}
