package ccu.command;

import java.util.ArrayList;

import ccu.general.ReadConfig;

public class Cmd_Group {
	// Temporary command save --> will be parsed further
	public static ArrayList<String[]> arrayGroupSave = new ArrayList<String[]>();

	// Saves whether it is a repeating or pulse block type
	public static ArrayList<String> arrayBlockTypeSave = new ArrayList<String>();

	// setblock save (the initial block that's placed down)
	public static ArrayList<String> arraySetblockSave = new ArrayList<String>();

	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Cmd_Group(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		/**
		 * This mostly just gets the name in the curly brackets, checks for more
		 * statements, and then puts the commands in an array and returns null
		 * Arguments:
		 * "PULSE" and "CLOCK" to specify type
		 */
		// System.out.println("LINE " + fullLineGet);

		boolean gotParam = false;
		String setblockCalc = null;
		boolean validBlock = false;

		ReadCCUFile ccuSubsetFile = new ReadCCUFile(this.arrayGet, tabNum);
		ArrayList<String> checkCommandsArray = ccuSubsetFile.checkCommands();
		if (checkCommandsArray != null && checkCommandsArray.isEmpty() == false) {
			this.arrayGet = checkCommandsArray;
		}

		// Removes "GROUP " and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("GROUP", "").replaceAll("^\\s+", "");
		if (statementEncase.startsWith("{") && statementEncase.endsWith("}:")) {
			String statementArgs = statementEncase.substring(1, statementEncase.length() - 2);

			// tests if the statementArgs has "PULSE" or "GROUP" at the beginning
			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "PULSE":
					arrayBlockTypeSave.add("command_block");
					// removes PULSE
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					gotParam = true;
					break;

				case "CLOCK":
					arrayBlockTypeSave.add("repeating_command_block");
					// removes CLOCK
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
					gotParam = true;
					break;

				case "BLOCK":
					// removes BLOCK
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());

					if (statementArgs.contains(" ") == false) {
						System.out.println("ERROR: Invalid arguments for 'BLOCK' in line '" + this.fullLineGet + "'");
						System.exit(0);
					}

					setblockCalc = statementArgs.substring(0, statementArgs.indexOf(" "));

					// checks whether it's a valid block - if not, ERROR
					for (String block : ReadConfig.blockArray) {
						if (setblockCalc.equals(block)) {
							validBlock = true;
							break;
						}
					}
					if (validBlock == false) {
						System.out.println("ERROR: Line '" + this.fullLineGet + "' contains an invalid block type");
						System.exit(0);
					}

					// removes setblock
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());

					// checks whether an int would work
					if (statementArgs.contains(" ")) {
						try {
							Integer.parseInt(statementArgs.substring(0, statementArgs.indexOf(" ")));
							setblockCalc = setblockCalc + " " + statementArgs.substring(0, statementArgs.indexOf(" "));

							// removes the number
							statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
						} catch (NumberFormatException e) {
							setblockCalc = setblockCalc + " " + 0;
						}
					} else {
						setblockCalc = setblockCalc + " " + 0;
					}

					// Adds setblock type
					arraySetblockSave.add(setblockCalc);
					break;
				}
			}

			if (statementArgs.contains(" ")) {
				switch (statementArgs.substring(0, statementArgs.indexOf(" "))) {
				case "PULSE":
					if (gotParam == false) {
						arrayBlockTypeSave.add("command_block");
						// removes PULSE
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
						gotParam = true;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;

				case "CLOCK":
					if (gotParam == false) {
						arrayBlockTypeSave.add("repeating_command_block");
						// removes CLOCK
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
						gotParam = true;
					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
						System.exit(0);
					}
					break;

				case "BLOCK":
					// removes BLOCK
					statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());

					if (setblockCalc == null) {
						if (statementArgs.contains(" ") == false) {
							System.out.println("ERROR: Invalid arguments for 'BLOCK' in line '" + this.fullLineGet + "'");
							System.exit(0);
						}
						setblockCalc = statementArgs.substring(0, statementArgs.indexOf(" "));

						// checks whether it's a valid block - if not, ERROR
						for (String block : ReadConfig.blockArray) {
							if (setblockCalc.equals(block)) {
								validBlock = true;
								break;
							}
						}
						if (validBlock == false) {
							System.out.println("ERROR: Line '" + this.fullLineGet + "' contains an invalid block type");
							System.exit(0);
						}

						// removes setblock
						statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());

						// checks whether an int would work
						if (statementArgs.contains(" ")) {
							try {
								Integer.parseInt(statementArgs.substring(0, statementArgs.indexOf(" ")));
								setblockCalc = setblockCalc + " " + statementArgs.substring(0, statementArgs.indexOf(" "));

								// removes the number
								statementArgs = statementArgs.substring(statementArgs.indexOf(" ") + 1, statementArgs.length());
							} catch (NumberFormatException e) {
								setblockCalc = setblockCalc + " " + 0;
							}
						} else {
							setblockCalc = setblockCalc + " " + 0;
						}

						// Adds setblock type
						arraySetblockSave.add(setblockCalc);
						break;

					} else {
						System.out.println(
								"ERROR: There are two arguments that conflict with each other in line '" + this.fullLineGet + "'");
					}

				}
			}

			// if setblock type is null, adds regular option
			if (setblockCalc == null) {
				arraySetblockSave.add(Var_Options.blockOption);
			}

			// tests for any spaces in the group name
			if (statementArgs.contains(" ") || statementArgs.contains("\t")) {
				System.out.println("ERROR: Arguments in line '" + this.fullLineGet + "' contains unnecessary spaces");
				System.exit(0);
			}

			// tests if the group name suffix ends with anything given in the .ini file
			if (gotParam == false) {
				for (String line : ReadConfig.groupSuffixPulse) {
					if (statementArgs.length() >= line.length()
							&& statementArgs.substring(statementArgs.length() - line.length()).equals(line)) {
						arrayBlockTypeSave.add("command_block");
						gotParam = true;
						break;
					}
				}
				for (String line : ReadConfig.groupSuffixRepeating) {
					if (statementArgs.length() >= line.length()
							&& statementArgs.substring(statementArgs.length() - line.length()).equals(line)) {
						arrayBlockTypeSave.add("repeating_command_block");
						gotParam = true;
						break;
					}
				}
			}

			if (gotParam == false) {
				System.out.println("WARNING: Group " + statementArgs + " contains no indicator for group type (defaults to PULSE)");
				arrayBlockTypeSave.add("command_block");
			}

			// Creates the string array, and puts it in the arraylist
			// Notice how the first element in each array is the group name and not a valid command

			String[] arrayGroup = new String[this.arrayGet.size() + 1];
			arrayGroup[0] = statementArgs;
			for (int i = 0; i < this.arrayGet.size(); i++) {

				// Checking tab spaces
				String whitespaceCalc = this.arrayGet.get(i).substring(0,
						(this.arrayGet.get(i).length() - this.arrayGet.get(i).replaceAll("^\\s+", "").length()));
				if (whitespaceCalc.contains(" ")) {
					System.out.println("ERROR: Line '" + this.arrayGet.get(i) + "' contains spaces instead of tab spaces");
					System.exit(0);
				}

				if (whitespaceCalc.length() - whitespaceCalc.replace("\t", "").length() != this.tabNum) {
					System.out.println("ERROR: Line '" + this.arrayGet.get(i) + "' contains an incorrect number of tab spaces");
					System.exit(0);
				}

				arrayGroup[i + 1] = this.arrayGet.get(i).replaceAll("^\\s+", "");
			}

			arrayGroupSave.add(arrayGroup);

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		for (int i = 0; i < arrayGroupSave.size(); i++) {
			for (int j = 0; j < arrayGroupSave.size(); j++) {
				if (i != j && arrayGroupSave.get(i)[0].equals(arrayGroupSave.get(j)[0])) {
					System.out.println("ERROR: '" + arrayGroupSave.get(j)[0] + "' is repeated as a group name");
					System.exit(0);
				}
			}
		}

		// should always return null
		return null;
	}
}
