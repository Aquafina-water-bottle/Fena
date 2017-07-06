package ccu.command;

import java.util.ArrayList;

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

		ReadCCUFile ccuSubsetFile = new ReadCCUFile(this.arrayGet, tabNum);
		ArrayList<String> checkCommandsArray = ccuSubsetFile.checkCommands();
		if (checkCommandsArray != null && checkCommandsArray.isEmpty() == false) {
			this.arrayGet = checkCommandsArray;
		}

		// Removes "LOOP" and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("LOOP", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {
			
			/*
			Boolean useAtBeg = null;
			Boolean noSpace = null;

			// Gets parameters
			String statementArgs = statementEncase.substring(1, statementEncase.length() - 2);
			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "BEG":
					useAtBeg = true;
					// removes BEG
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "END":
					useAtBeg = false;
					// removes END
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "NOSPACE":
					noSpace = true;
					// removes NOSPACE
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;
				}
			}

			// Gets second parameters
			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "BEG":
					if (useAtBeg == null) {
						useAtBeg = true;
					} else {
						System.out.println("ERROR: There are two parameters that conflict with each other in line '"
								+ this.fullLineGet + "'");
					}
					// removes BEG
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "END":
					if (useAtBeg == null) {
						useAtBeg = false;
					} else {
						System.out.println("ERROR: There are two parameters that conflict with each other in line '"
								+ this.fullLineGet + "'");
					}
					// removes END
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;

				case "NOSPACE":
					if (noSpace == null) {
						noSpace = true;
					} else {
						System.out.println("ERROR: There are two parameters that conflict with each other in line '"
								+ this.fullLineGet + "'");
					}
					// removes NOSPACE
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					break;
				}
				// the end should make 'statementArgs' as the actual use thing
			}
			
			// sets default values if parameter options aren't used
			if (useAtBeg == null) {
				useAtBeg = true;
			}
			if (noSpace == null) {
				noSpace = false;
			}
			

			for (int i = 0; i < this.arrayGet.size(); i++) {
				// Checking tab spaces
				String whitespaceCalc = this.arrayGet.get(i).substring(0,
						(this.arrayGet.get(i).length() - this.arrayGet.get(i).replaceAll("^\\s+", "").length()));
				if (whitespaceCalc.contains(" ")) {
					System.out.println(
							"ERROR: Line '" + this.arrayGet.get(i) + "' contains spaces instead of tab spaces");
					System.exit(0);
				}

				if (whitespaceCalc.length() - whitespaceCalc.replace("\t", "").length() != this.tabNum) {
					System.out.println(
							"ERROR: Line '" + this.arrayGet.get(i) + "' contains an incorrect number of tab spaces");
					System.exit(0);
				}

				String newString = null;
				String newStringCalc = null;
				// checks for conditional settings
				// this is the main part where the "USE" gets put into place
				
				newString = whitespaceCalc.substring(1, whitespaceCalc.length());
				
				// if conditional
				if (this.arrayGet.get(i).replaceAll("^\\s+", "").contains("CCU_COND_")) {
					newStringCalc = this.arrayGet.get(i).replaceAll("^\\s+", "").replace("CCU_COND_", "");
					newString = newString + "CCU_COND_";
				} else {
					newStringCalc = this.arrayGet.get(i).replaceAll("^\\s+", "");
				}

				
				// whether it is at the beginning or at the end
				// seperates into whether noSpace is true or not
				if (useAtBeg == true) {
					if (noSpace == true) {
						newString = newString + statementArgs + newStringCalc;
					} else {
						newString = newString + statementArgs + " " + newStringCalc;
					}
				} else {
					if (noSpace == true) {
						newString = newString + newStringCalc + statementArgs;
					} else {
						newString = newString + newStringCalc + " " + statementArgs;
					}
				}
				
				arrayUseReturn.add(newString);
			}*/

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		return arrayLoopReturn;
	}
}
