package ccu.command;

import java.io.File;
import java.util.ArrayList;
import java.util.regex.Pattern;

import ccu.general.GeneralFile;
import ccu.general.ReadConfig;

public class ReadCCUFile {
	private ArrayList<String> ccuFileArray = new ArrayList<String>();
	private int tabNum = 0;
	// private ArrayList<String> tempOptionArrayList;
	// private ArrayList<String> removeOptionArrayList;

	// Setting initialization
	/*
	String blockOption = null;
	Coordinates coordsOption = new Coordinates(0, 0, 0);
	String styleOption = null;
	boolean parseOption = false;
	boolean commandOption = false;
	boolean compilerOption = false;
	File filePathFuncOption = null;
	boolean preserveCoordsOption = false;
	*/

	// Constructor
	public ReadCCUFile(File fileName) {
		GeneralFile ccuFile = new GeneralFile(fileName);
		this.ccuFileArray = GeneralFile.removeSkipLineBlock(
				GeneralFile.removeComment(GeneralFile.removeCommentBlock(ccuFile.getFileArray(), "//=", "=//"), "//"), "/*", "*/");
		// .replaceAll("\\s+$", "")
	}

	public ReadCCUFile(ArrayList<String> arrayName, int tabNumGet) {
		this.ccuFileArray = arrayName;
		this.tabNum = tabNumGet;
	}

	// @formatter:off
	private static final String[] cmdArray = {
			"MFUNC",
			"GROUP",
			"DEF",
			// "FUNC",
			// "ARRAY",
			// "OPTIONS",
			// "OBJADD",
			// "OBJREV",
			"OPTIONS",
			// "TEAMADD",
			// "TEAMREV",
			// "LOOP",
			// "IF",
			// "ELIF",
			// "ELSE",
			"USE",
			"COND"
			};
	// @formatter:on

	private final static int STRING = 0;
	private final static int INT = 1;
	private final static int SELECTOR = 2;
	private final static int DATATAG = 3;

	/*
	 *  proposal on how this will work:
	 * each statement will have its own object
	 * reoccuring method for checkCommands()
	 * 
	 * 3 types of statements:
	 * CMD - Holds commands (GROUP, MFUNC)
	 * 		-These always return NULL once ran
	 * CON - Control flow (USE, IF, ELIF, ELSE, LOOP, COND)
	 * 		-These normally return statements once ran
	 * VAR - Variables (ARRAY, DEF, FUNC, OBJADD, OBJREV, TEAMADD, TEAMREV, OPTIONS)
	 * 		-These always returns NULL once ran
	 * 
	 * Eg:
	 * checkCommands()
	 * 	-GROUP
	 * 		-ARRAY
	 * 			-USE
	 * 
	 * -checkCommands() is a recurring method
	 * -It will detect the first statement, and send the encapsulated array to the group .getArray() method
	 * -Since the getArray() method also contains checkCommands, it will send it off to the array .getArray() method
	 * -Repeat until the most encapsulated array is sent, which in this case, is 'USE'
	 * -Therefore, 'USE' is parsed first
	 * -The USE thing is parsed, and then the array, and then the group
	 * -The USE will return something for ARRAY, ARRAY returns null, and GROUP returns null
	 */

	public ArrayList<String> checkCommands() {
		int indexCalc = 0;
		int subListCalc1 = -2;
		int subListCalc2 = -2;
		Integer resetIndex = null;
		boolean resetArray = false;
		boolean singleLineStatement = false;
		boolean recheckLine = false;
		boolean resetDefIndex = false;
		String firstDefinition = null;
		String defineLineCalc = null;
		String[] defineParamsCalc = null;
		String definitionCalc = null;
		boolean getStatement = false;

		ArrayList<String> getCalcArray = new ArrayList<String>();
		ArrayList<String> encapsulateArray = new ArrayList<String>();
		ArrayList<String> subListTopArray = new ArrayList<String>();
		ArrayList<String> subListBottomArray = new ArrayList<String>();

		// TODO
		// Implements any defines, functions, arrays here with the only exceptions being / at the beginning and inside definitions
		// ResetIndex and break from the loop if defines / functions / arrays / imports are found

		// if the define is within it, and the tabnum is less than or equal to define tab num

		for (int i = 0; i < this.ccuFileArray.size(); i++) {
			// Resets getStatement
			getStatement = false;

			// Resets index as resetting it at the bottom did not work
			if (resetIndex != null) {
				i = resetIndex + 0;
				resetIndex = null;
			}

			// does at least once to check if it works
			do {
				firstDefinition = null;
				defineLineCalc = null;
				defineParamsCalc = null;
				definitionCalc = null;
				// iterates through all definitions
				// starts at the negative end to prioritize the more tabulated definition
				for (int defIndex = Var_Define.arrayDefineSave.size() - 1; defIndex >= 0; defIndex--) {

					// if a definition matches up
					// System.out.println(this.tabNum + " | " + VAR_Define.arrayDefineSave.get(defIndex)[1] + " | " + ccuFileArray.get(i));
					if (ccuFileArray.get(i).trim().contains(Var_Define.arrayDefineSave.get(defIndex)[2])
							&& this.tabNum >= Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[1])
							&& ccuFileArray.get(i).trim().substring(0, 3).equals("DEF") == false) {
						recheckLine = true;

						// get anything past the definition
						defineLineCalc = ccuFileArray.get(i)
								.substring(ccuFileArray.get(i).indexOf(Var_Define.arrayDefineSave.get(defIndex)[2])
										+ Var_Define.arrayDefineSave.get(defIndex)[2].length());

						// checks if there are parameters in the first place
						if (Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[4]) > 0) {

							// if there is stuff past the definition and has () in the correct order
							if (defineLineCalc.isEmpty() == false && defineLineCalc.contains("(") && defineLineCalc.contains(")")
									&& defineLineCalc.indexOf("(") < defineLineCalc.indexOf(")")) {

								// split params
								defineParamsCalc = defineLineCalc.substring(defineLineCalc.indexOf("(") + 1, defineLineCalc.indexOf(")"))
										.split(";");

								// set params
								definitionCalc = Var_Define.arrayDefineSave.get(defIndex)[3];
								for (int paramIndex = 0; paramIndex < defineParamsCalc.length; paramIndex++) {
									definitionCalc = definitionCalc.replace("|" + paramIndex + "|", defineParamsCalc[paramIndex]);
								}

								// remove unnecessary params
								if (defineParamsCalc.length < Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[4])) {
									for (int paramIndex = defineParamsCalc.length; paramIndex <= Integer
											.parseInt(Var_Define.arrayDefineSave.get(defIndex)[4]); paramIndex++) {
										definitionCalc = definitionCalc.replace("|" + paramIndex + "|", "");
									}
								}

								// replace params
								defineLineCalc = ccuFileArray.get(i).substring(0, ccuFileArray.get(i).indexOf("("))
										+ ccuFileArray.get(i).substring(ccuFileArray.get(i).indexOf(")") + 1);
								defineLineCalc = defineLineCalc.replaceFirst(Pattern.quote(Var_Define.arrayDefineSave.get(defIndex)[2]),
										definitionCalc);
								ccuFileArray.set(i, defineLineCalc);

							} else {
								// replace all params
								definitionCalc = Var_Define.arrayDefineSave.get(defIndex)[3];
								for (int paramIndex = 0; paramIndex <= Integer
										.parseInt(Var_Define.arrayDefineSave.get(defIndex)[4]); paramIndex++) {
									definitionCalc = definitionCalc.replace("|" + paramIndex + "|", "");
								}

								defineLineCalc = ccuFileArray.get(i)
										.replaceFirst(Pattern.quote(Var_Define.arrayDefineSave.get(defIndex)[2]), definitionCalc);
								ccuFileArray.set(i, defineLineCalc);
							}
						} else {
							// sets it as is because params aren't an issue
							ccuFileArray.set(i, ccuFileArray.get(i).replaceFirst(Pattern.quote(Var_Define.arrayDefineSave.get(defIndex)[2]),
									Var_Define.arrayDefineSave.get(defIndex)[3]));
						}

						// tests for recurring definition
						if (firstDefinition != null && firstDefinition.equals(Var_Define.arrayDefineSave.get(defIndex)[3])) {
							System.out.println("ERROR: Recurring definition at line '" + ccuFileArray.get(i) + "'"
									+ "starting with the definition '" + firstDefinition + "'");
							System.exit(0);
						}

						// stores in case of a recurring definition
						if (firstDefinition == null) {
							firstDefinition = Var_Define.arrayDefineSave.get(defIndex)[3];
						}
						break;
					} else {
						recheckLine = false;
					}
				}
			} while (recheckLine);

			for (String statement : ReadCCUFile.cmdArray) {
				singleLineStatement = false;

				// detects whether it is a proper statement
				if (ccuFileArray.get(i).length() >= (statement.length() + this.tabNum)
						&& ccuFileArray.get(i).substring(this.tabNum, statement.length() + this.tabNum).equals(statement)) {

					// gets statement
					String statementTest = ccuFileArray.get(i).substring(this.tabNum, statement.length() + this.tabNum);

					// TODO: Will gather DEF, IMPORT, TEAMREV, OBJREV in this area
					// This is to get the array for said statement

					switch (statementTest) {
					case "DEF":
						Var_Define objDefine = new Var_Define(ccuFileArray.get(i), this.tabNum);
						getCalcArray = objDefine.getArray();
						resetArray = true;
						singleLineStatement = true;

						// case "IMPORT":

						// case "OBJREV":

						// case "TEAMREV":

					}

					// only one line
					if (singleLineStatement == true) {
						if (i > 0) {
							subListTopArray = new ArrayList<String>(this.ccuFileArray.subList(0, i));
							// System.out.println(subListTopArray);
						} else {
							subListTopArray.clear();
						}
						subListBottomArray = new ArrayList<String>(this.ccuFileArray.subList(i + 1, this.ccuFileArray.size()));
						// System.out.println(subListBottomArray);

					} else { // given in an encapsulation array
						this.tabNum++;
						indexCalc = i;

						// clears array whenever it gets filled by detecting a statement
						encapsulateArray.clear();

						// gets encapsulation array by detecting the number of tab spaces
						// tl;dr if it has a min number of tab spaces as stated, it will be added
						while (true) {
							indexCalc++;

							// if proper number of tabnums and not past size limit
							if (indexCalc < this.ccuFileArray.size() && ccuFileArray.get(indexCalc).substring(0, this.tabNum).length()
									- ccuFileArray.get(indexCalc).substring(0, this.tabNum).replace("\t", "").length() == this.tabNum) {

								// Starting process of getting the top/bottom array index numbers
								// Also adds the line to the encapsulation array
								encapsulateArray.add(this.ccuFileArray.get(indexCalc));
								if (subListCalc1 == -2) {
									subListCalc1 = indexCalc - 1;
								}
							} else {
								subListCalc2 = indexCalc;
								break;
							}
						}

						/* Sublists
						 * sublists are used to split the array into two or three parts
						 * The top and bottom will be seperated from the encapsulated array
						 * while the encapsulated array is sent off to be parsed on its own
						 * 
						 * if the encapsulated array returns with an array, the array will be inserted between the top and bottom arrays
						 * yet if it returns null, it's just the top and bottom arrays
						 */

						subListTopArray.clear();
						subListBottomArray.clear();

						// actually creates the top / bottom sublists
						if (subListCalc1 >= 0) {
							subListTopArray = new ArrayList<String>(this.ccuFileArray.subList(0, subListCalc1));
						}
						subListBottomArray = new ArrayList<String>(this.ccuFileArray.subList(subListCalc2, this.ccuFileArray.size()));
						subListCalc1 = -2;
						subListCalc2 = -2;

						// detect if the encapsulated array size is 0
						if (encapsulateArray.size() == 0) {
							System.out.println("WARNING: " + statementTest + " has 0 commands at line '" + ccuFileArray.get(i) + "'");
							break;
						}

						// System.out.println(encapsulateArray);

						// switch case for all statements with encapsulation
						switch (statementTest) {
						case "MFUNC":
							Cmd_MFunc objMFunc = new Cmd_MFunc(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objMFunc.getArray();
							resetArray = true;
							break;

						case "GROUP":
							Cmd_Group objGroup = new Cmd_Group(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objGroup.getArray();
							resetArray = true;
							break;

						case "OPTIONS":
							Var_Options objOptions = new Var_Options(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objOptions.getArray();
							resetArray = true;
							break;

						case "USE":
							Con_Use objUse = new Con_Use(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objUse.getArray();
							resetArray = true;
							break;

						case "COND":
							Con_Cond objCond = new Con_Cond(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objCond.getArray();
							resetArray = true;
							break;
						}
					}
				}

				// Reset all definitions according to tabnum when resetArray exists
				if (resetArray) {
					getStatement = true;
					// combines any given arrays
					this.ccuFileArray.clear();
					if (getCalcArray == null || getCalcArray.size() == 0) {
						for (String line : subListTopArray) {
							this.ccuFileArray.add(line);
						}

						for (String line : subListBottomArray) {
							this.ccuFileArray.add(line);
						}
					} else {
						for (String line : subListTopArray) {
							this.ccuFileArray.add(line);
						}
						for (String line : getCalcArray) {
							this.ccuFileArray.add(line);
						}
						for (String line : subListBottomArray) {
							this.ccuFileArray.add(line);
						}
					}

					// only resets when the the statement isn't a single line
					if (singleLineStatement == false) {

						// reset all definitions that don't work with the decreasing tab numbers
						for (int defIndex = 0; defIndex < Var_Define.arrayDefineSave.size(); defIndex++) {
							if (resetDefIndex == true) {
								resetDefIndex = false;
								defIndex = 0;
							}
							if (this.tabNum == Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[1])) {
								resetDefIndex = true;
								Var_Define.arrayDefineSave.remove(defIndex);
							}
						}

						indexCalc = 0;
						this.tabNum--;
					}

					// general reset
					resetArray = false;
					resetIndex = i + 0;
					break;
				}
			}
			if (getStatement == false) {
				String getWhiteSpace = null;
				String shortcutCalc = null;
				String[] shortcutCalcArray = null;
				int[] shortcutTypeArray = null;
				String shortcutResultCalc = null;
				boolean shortcutDataTag = false;
				boolean containsScoreboard = false;
				boolean changedLine = false;

				// Regular command - General shortcuts are done here
				// NOTICE: Execute and scoreboard shortcuts will be IGNORED if found in data tags
				// Also, scoreboard shortcuts can only happen once

				/* Scoreboard shortcuts (All selectors can be regular strings)
				 * scoreboard players add: @e[type=ArmorStand,RRStand] RRti + 1 {DisabledSlots:2096896}
				 * scoreboard players remove: @e[type=ArmorStand,RRStand] RRti - 1 {DisabledSlots:2096896}
				 * scoreboard players set: @e[type=ArmorStand,RRStand] RRti = 10 {DisabledSlots:2096896}
				 * scoreboard players operation: N/A - Define with ScOP
				 * scoreboard players test: @e[type=ArmorStand,RRStand] RRti ?
				 * scoreboard players test: @e[type=ArmorStand,RRStand] RRti ? 0 10
				 * scoreboard players reset: @e[type=ArmorStand,RRStand] reset RRti
				 * scoreboard players enable: @e[type=ArmorStand,RRStand] enable RRti
				 * scoreboard players tag @x add: @e[type=ArmorStand,RRStand] + RRTimer {Marker:1b}
				 * scoreboard players tag @x remove: @e[type=ArmorStand,RRStand] - RRTimer {Marker:1b}
				 * scoreboard teams join: RRd_y J> @e[type=ArmorStand,RRStand]
				 * scoreboard teams leave: RRd_y L> @e[type=ArmorStand,RRStand]
				 * scoreboard teams empty: RRd_y E>
				 */

				/* shortcutSelectorArray
				 * 0 = string
				 * 1 = int
				 * 2 = selector
				 * 3 = data tag
				 * 
				 * anything with a data tag, even with spaces will be 3 and not 0, 1 or 2
				 */

				getWhiteSpace = ccuFileArray.get(i).substring(0, tabNum);
				shortcutCalc = ccuFileArray.get(i).substring(tabNum);
				shortcutCalcArray = shortcutCalc.split(" ");
				shortcutTypeArray = new int[shortcutCalcArray.length];
				for (int j = 0; j < shortcutCalcArray.length; j++) {

					// if it's a data tag --> 3 (DATATAG)
					if (shortcutCalcArray[j].startsWith("{")) {
						shortcutDataTag = true;
					}
					if (shortcutDataTag == true) {
						shortcutTypeArray[j] = DATATAG;
						continue;
					}

					// if it's a number (as int) --> 1 (INT)
					try {
						Integer.parseInt(shortcutCalcArray[j]);
						shortcutTypeArray[j] = INT;
						continue;
					} catch (NumberFormatException e) {
					}

					// if it is a selector --> 2 (SELECTOR)
					for (String selectorGet : ReadConfig.selectorArray) {
						if (shortcutCalcArray[j].startsWith(selectorGet)) {
							shortcutTypeArray[j] = SELECTOR;
							break;
						}
					}

					// if it is 'scoreboard'
					if (shortcutCalcArray[j].startsWith("scoreboard")) {
						containsScoreboard = true;
						break;
					}
				}

				/*
				for (int j = 0; j < shortcutCalcArray.length; j++) {
					System.out.print(shortcutCalcArray[j] + " | " + shortcutTypeArray[j] + " | ");
				}
				System.out.println("");
				*/

				// Will do the scoreboard shortcut as long as 'scoreboard' is not present
				if (containsScoreboard == false) {
					for (int j = 0; j < shortcutCalcArray.length; j++) {

						// if it contains '+'
						if (shortcutCalcArray[j].equals("+") && shortcutTypeArray[j] == STRING) {

							// scoreboard players add
							if (j >= 2 && j + 1 < shortcutCalcArray.length && (shortcutTypeArray[j - 2] == (STRING) || shortcutTypeArray[j - 2] == (SELECTOR))
									&& shortcutTypeArray[j - 1] == STRING && shortcutTypeArray[j + 1] == INT) {
								shortcutCalcArray[j - 2] = "scoreboard players add " + shortcutCalcArray[j - 2] + " "
										+ shortcutCalcArray[j - 1] + " " + shortcutCalcArray[j + 1];
								shortcutCalcArray[j - 1] = "";
								shortcutCalcArray[j - 0] = "";
								shortcutCalcArray[j + 1] = "";
								changedLine = true;
								break;
							}

							// scoreboard players tag name add
							if (j >= 1 && j + 1 < shortcutCalcArray.length && shortcutTypeArray[j - 1] == (STRING)
									|| shortcutTypeArray[j - 1] == (SELECTOR) && shortcutTypeArray[j + 1] == STRING) {
								shortcutCalcArray[j - 1] = "scoreboard players tag " + shortcutCalcArray[j - 1] + " add "
										+ shortcutTypeArray[j + 1];
								shortcutCalcArray[j - 0] = "";
								shortcutCalcArray[j + 1] = "";
								changedLine = true;
								break;
							}
						}

						// if it contains '-'
						if (shortcutCalcArray[j].equals("-") && shortcutTypeArray[j] == STRING) {

							// scoreboard players remove
							if (j >= 2 && j + 1 < shortcutCalcArray.length && (shortcutTypeArray[j - 2] == (STRING) || shortcutTypeArray[j - 2] == (SELECTOR))
									&& shortcutTypeArray[j - 1] == STRING && shortcutTypeArray[j + 1] == INT) {
								shortcutCalcArray[j - 2] = "scoreboard players remove " + shortcutCalcArray[j - 2] + " "
										+ shortcutCalcArray[j - 1] + " " + shortcutCalcArray[j + 1];
								shortcutCalcArray[j - 1] = "";
								shortcutCalcArray[j - 0] = "";
								shortcutCalcArray[j + 1] = "";
								changedLine = true;
								break;
							}

							// scoreboard players tag name remove
							if (j >= 1 && j + 1 < shortcutCalcArray.length && (shortcutTypeArray[j - 1] == (STRING)
									|| shortcutTypeArray[j - 1] == (SELECTOR)) && shortcutTypeArray[j + 1] == STRING) {
								shortcutCalcArray[j - 1] = "scoreboard players tag " + shortcutCalcArray[j - 1] + " remove "
										+ shortcutTypeArray[j + 1];
								shortcutCalcArray[j - 0] = "";
								shortcutCalcArray[j + 1] = "";
								changedLine = true;
								break;
							}
						}

						// if it contains '='
						if (shortcutCalcArray[j].equals("=") && shortcutTypeArray[j] == STRING) {

							// scoreboard players set
							if (j >= 2 && j + 1 < shortcutCalcArray.length && (shortcutTypeArray[j - 2] == (STRING) || shortcutTypeArray[j - 2] == (SELECTOR))
									&& shortcutTypeArray[j - 1] == STRING && shortcutTypeArray[j + 1] == INT) {
								shortcutCalcArray[j - 2] = "scoreboard players set " + shortcutCalcArray[j - 2] + " "
										+ shortcutCalcArray[j - 1] + " " + shortcutCalcArray[j + 1];
								shortcutCalcArray[j - 1] = "";
								shortcutCalcArray[j - 0] = "";
								shortcutCalcArray[j + 1] = "";
								changedLine = true;
								break;
							}
						}

						// if it contains '?'
						if (shortcutCalcArray[j].equals("?") && shortcutTypeArray[j] == STRING) {

							// scoreboard players test
							if (j >= 2 && j + 1 < shortcutCalcArray.length && (shortcutTypeArray[j - 2] == (STRING) || shortcutTypeArray[j - 2] == (SELECTOR))
									&& shortcutTypeArray[j - 1] == STRING && shortcutTypeArray[j + 1] == INT) {
								shortcutCalcArray[j - 2] = "scoreboard players test " + shortcutCalcArray[j - 2] + " "
										+ shortcutCalcArray[j - 1] + " " + shortcutCalcArray[j + 1];
								shortcutCalcArray[j - 1] = "";
								shortcutCalcArray[j - 0] = "";
								shortcutCalcArray[j + 1] = "";
								changedLine = true;
								break;
							}
						}

						// if it contains 'reset' or 'enable'
						if (shortcutCalcArray[j].equals("reset")
								|| shortcutCalcArray[j].equals("enable") && shortcutTypeArray[j] == STRING) {

							// scoreboard players reset or enable
							if (j >= 1 && j + 1 < shortcutCalcArray.length && (shortcutTypeArray[j - 1] == (STRING)
									|| shortcutTypeArray[j - 1] == (SELECTOR)) && shortcutTypeArray[j + 1] == STRING) {
								shortcutCalcArray[j - 1] = "scoreboard players " + shortcutCalcArray[j] + " " + shortcutCalcArray[j - 1]
										+ " " + shortcutTypeArray[j + 1];
								shortcutCalcArray[j - 0] = "";
								shortcutCalcArray[j + 1] = "";
								changedLine = true;
								break;
							}
						}

						// if it contains 'J>'
						if (shortcutCalcArray[j].equals("J>") && shortcutTypeArray[j] == STRING) {

							// scoreboard teams join
							if (j >= 1 && j + 1 < shortcutCalcArray.length && shortcutTypeArray[j - 1] == STRING && shortcutTypeArray[j + 1] == (STRING)
									|| shortcutTypeArray[j + 1] == (SELECTOR)) {
								shortcutCalcArray[j - 1] = "scoreboard teams join " + shortcutCalcArray[j - 1] + " "
										+ shortcutCalcArray[j + 1];
								shortcutCalcArray[j - 0] = "";
								shortcutCalcArray[j + 1] = "";
								changedLine = true;
								break;
							}
						}

						// if it contains 'L>'
						if (shortcutCalcArray[j].equals("L>") && shortcutTypeArray[j] == STRING) {

							// scoreboard teams leave
							if (j >= 1 && j + 1 < shortcutCalcArray.length && shortcutTypeArray[j - 1] == STRING && (shortcutTypeArray[j + 1] == (STRING)
									|| shortcutTypeArray[j + 1] == (SELECTOR))) {
								shortcutCalcArray[j - 1] = "scoreboard teams leave " + shortcutCalcArray[j - 1] + " "
										+ shortcutCalcArray[j + 1];
								shortcutCalcArray[j - 0] = "";
								shortcutCalcArray[j + 1] = "";
								changedLine = true;
								break;
							}
						}

						// if it contains 'E>'
						if (shortcutCalcArray[j].equals("E>") && shortcutTypeArray[j] == STRING) {
							// scoreboard teams leave
							if (j >= 1 && shortcutTypeArray[j - 1] == STRING) {
								shortcutCalcArray[j - 1] = "scoreboard teams empty " + shortcutCalcArray[j - 1];
								shortcutCalcArray[j - 0] = "";
								changedLine = true;
								break;
							}
						}
					}
				}

				if (changedLine == true) {
					for (int j = 0; j < shortcutCalcArray.length; j++)
						if (j == 0) {
							shortcutResultCalc = getWhiteSpace + shortcutCalcArray[j];
						} else {
							if (shortcutCalcArray[j].equals("") == false) {
								shortcutResultCalc += " " + shortcutCalcArray[j];
							}
						}
					ccuFileArray.set(i, shortcutResultCalc);
				}
			}
		}
		return ccuFileArray;
	}
}
