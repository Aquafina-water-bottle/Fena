package ccu.command;

import java.util.ArrayList;

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

		ReadCCUFile ccuSubsetFile = new ReadCCUFile(this.arrayGet, tabNum);
		ArrayList<String> checkCommandsArray = ccuSubsetFile.checkCommands();
		if (checkCommandsArray != null && checkCommandsArray.isEmpty() == false) {
			this.arrayGet = checkCommandsArray;
		}

		// Removes "COND " and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("COND", "").replaceAll("^\\s+", "");
		if (statementEncase.endsWith(":")) {
			for (int i = 0; i < this.arrayGet.size(); i++) {
				// Checking tab spaces
				String whitespaceCalc = this.arrayGet.get(i).substring(0,
						(this.arrayGet.get(i).length() - this.arrayGet.get(i).replaceAll("^\\s+", "").length()));
				if (whitespaceCalc.contains(" ")) {
					System.out.println(
							"ERROR: Line '" + this.arrayGet.get(i) + "' contains spaces instead of tab spaces");
					System.exit(0);
				}

				if (whitespaceCalc.length() - whitespaceCalc.replaceAll("\t", "").length() != this.tabNum) {
					System.out.println(
							"ERROR: Line '" + this.arrayGet.get(i) + "' contains an incorrect number of tab spaces");
					System.exit(0);
				}

				// Adds "CCU_COND_" in front of each command assuming it isn't already in the front

				String newString = null;

				if (this.arrayGet.get(i).replaceAll("^\\s+", "").contains("CCU_COND_")) {
					newString = this.arrayGet.get(i).replace("CCU_COND_", "");
					newString = whitespaceCalc.substring(1, whitespaceCalc.length()) + "CCU_COND_"
							+ newString.replace(whitespaceCalc, "");
				} else {
					// Puts CCU_COND_ before the thing
					newString = whitespaceCalc.substring(1, whitespaceCalc.length()) + "CCU_COND_"
							+ this.arrayGet.get(i).replace(whitespaceCalc, "");
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
