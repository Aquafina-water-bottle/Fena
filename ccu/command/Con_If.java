package ccu.command;

import java.util.ArrayList;

public class Con_If {
	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Con_If(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		/** Essentially runs the given array if the arguments return true
		 * The majority of that will be parsed in the MathParser class
		 * 
		 * Examples:
		 * IF {1 + 3 = 4 && 3 + 1 = 2 + 2 || 3 + 2 = 5}
		 * 
		 * 
		 */

		// Removes "IF" and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("IF", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {
			
			
			
			
			
		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		// To prevent lag, checkCommands() is done ONLY after the first part of the IF command returns true
		ReadCCUFile ccuSubsetFile = new ReadCCUFile(this.arrayGet, tabNum);
		ArrayList<String> checkCommandsArray = ccuSubsetFile.checkCommands();
		if (checkCommandsArray != null && checkCommandsArray.isEmpty() == false) {
			this.arrayGet = checkCommandsArray;
		}

		return null;
	}
}
