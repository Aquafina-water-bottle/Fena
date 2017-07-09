package ccu.command;

import java.util.ArrayList;

import ccu.general.ArgUtils;

public class Con_Use {
	private ArrayList<String> arrayUseReturn = new ArrayList<String>();
	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Con_Use(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		/** Puts characters at the end or beginning of a command
		 * Possible parameters: 
		 * {asdfasdf} --> defaults to {BEG asdfasdf} 
		 * {BEG asdfasdf} --> adds asdfasdf to the beginning of a command
		 * {NOSPACE asdfasdf} --> adds asdfasdf without the space seperation
		 * {END asdfasdf} --> adds asdfasdf to the end of a command
		 * Mix/match the parameters (if there are identical parameters, error)
		 * Cannot be both "BEG" and "END"
		 */
		// System.out.println("LINE " + fullLineGet);

		ReadCCUFile ccuSubsetFile = new ReadCCUFile(this.arrayGet, tabNum);
		ArrayList<String> checkCommandsArray = ccuSubsetFile.checkCommands();
		if (checkCommandsArray != null && checkCommandsArray.isEmpty() == false) {
			this.arrayGet = checkCommandsArray;
		}

		// Removes "USE" and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("USE", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {

			Boolean useAtBeg = null;
			Boolean noSpace = null;

			// Gets parameters
			String statementArgs = statementEncase.substring(1, statementEncase.length() - 2);
			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "BEG":
					useAtBeg = true;
					// removes BEG
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "END":
					useAtBeg = false;
					// removes END
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "NOSPACE":
					noSpace = true;
					// removes NOSPACE
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
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
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					}
					// removes BEG
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "END":
					if (useAtBeg == null) {
						useAtBeg = false;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					}
					// removes END
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
					break;

				case "NOSPACE":
					if (noSpace == null) {
						noSpace = true;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					}
					// removes NOSPACE
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1);
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
			
			// Checking tab spaces
			String whitespaceCalc = ArgUtils.checkWhiteSpace(this.arrayGet, this.tabNum);

			for (int i = 0; i < this.arrayGet.size(); i++) {
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
				/*
					if (noSpace == true) {
						// without spaces and not conditional
						newString = newString + statementArgs
								+ this.arrayGet.get(i).replace(whitespaceCalc, "");
					} else {
						// with spaces and not conditional
						newString = newString + statementArgs
								+ " " + this.arrayGet.get(i).replace(whitespaceCalc, "");
					}
				}*/

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
			}

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		return arrayUseReturn;
	}
}
