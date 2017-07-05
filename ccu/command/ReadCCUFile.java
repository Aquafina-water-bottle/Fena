package ccu.command;

import java.io.File;
import java.util.ArrayList;
import java.util.regex.Pattern;

import ccu.general.GeneralFile;
import ccu.general.ReadConfig;
import ccu.mcfunction.FunctionNick;

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
			"FUNC",
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
		String defineLineCalc = null;
		String[] defineParamsCalc = null;
		String definitionCalc = null;
		boolean getStatement = false;
		String definitionSave = null;
		Integer defineCoordsCalc = null;
		Integer begIndexCalc = null;
		Integer endIndexCalc = null;

		ArrayList<String> usedDefinitionArray = new ArrayList<String>();
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
			usedDefinitionArray.clear();
			do {
				defineLineCalc = null;
				defineParamsCalc = null;
				definitionCalc = null;
				definitionSave = null;
				begIndexCalc = null;
				endIndexCalc = null;

				// iterates through all definitions
				// starts at the negative end to prioritize the more tabulated definition
				for (int defIndex = Var_Define.arrayDefineSave.size() - 1; defIndex >= 0; defIndex--) {

					// System.out.println(this.tabNum + " | " + VAR_Define.arrayDefineSave.get(defIndex)[1] + " | " + ccuFileArray.get(i));

					// when the line starts with 'DEF'
					if (ccuFileArray.get(i).trim().substring(0, 3).equals("DEF") == true) {
						definitionSave = ccuFileArray.get(i);
						ccuFileArray.set(i, definitionSave.substring(Var_Define.getDefineIndex(definitionSave)));
					}

					// if a definition matches up
					if (ccuFileArray.get(i).trim().contains(Var_Define.arrayDefineSave.get(defIndex)[2])
							&& this.tabNum >= Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[1])) {
						recheckLine = true;

						// calcs firstIndexCalc and lastIndexCalc
						begIndexCalc = ccuFileArray.get(i).indexOf(Var_Define.arrayDefineSave.get(defIndex)[2]);
						endIndexCalc = ccuFileArray.get(i).indexOf(Var_Define.arrayDefineSave.get(defIndex)[2])
								+ Var_Define.arrayDefineSave.get(defIndex)[3].length();

						// if it is 'DEF'
						if (definitionSave != null) {
							begIndexCalc += Var_Define.getDefineIndex(definitionSave);
							endIndexCalc += Var_Define.getDefineIndex(definitionSave);
						}

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
								defineParamsCalc = defineLineCalc
										.substring(defineLineCalc.indexOf("(") + 1, defineLineCalc.indexOf(")")).split(";");

								// set params
								definitionCalc = Var_Define.arrayDefineSave.get(defIndex)[3];
								for (int paramIndex = 0; paramIndex < defineParamsCalc.length; paramIndex++) {
									if (definitionCalc.contains("|" + paramIndex + "|")) {
										endIndexCalc -= ("|" + paramIndex + "|").length();
										endIndexCalc += defineParamsCalc[paramIndex].length();
										definitionCalc = definitionCalc.replace("|" + paramIndex + "|", defineParamsCalc[paramIndex]);
									}
								}

								// remove unnecessary params
								if (defineParamsCalc.length < Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[4])) {
									for (int paramIndex = defineParamsCalc.length; paramIndex <= Integer
											.parseInt(Var_Define.arrayDefineSave.get(defIndex)[4]); paramIndex++) {
										if (definitionCalc.contains("|" + paramIndex + "|")) {
											endIndexCalc -= ("|" + paramIndex + "|").length();
											definitionCalc = definitionCalc.replace("|" + paramIndex + "|", "");
										}

									}
								}

								// replace params
								defineLineCalc = ccuFileArray.get(i).substring(0, ccuFileArray.get(i).indexOf("("))
										+ ccuFileArray.get(i).substring(ccuFileArray.get(i).indexOf(")") + 1);
								defineLineCalc = defineLineCalc
										.replaceFirst(Pattern.quote(Var_Define.arrayDefineSave.get(defIndex)[2]), definitionCalc);
								ccuFileArray.set(i, defineLineCalc);

							} else {
								// replace all params
								definitionCalc = Var_Define.arrayDefineSave.get(defIndex)[3];
								for (int paramIndex = 0; paramIndex <= Integer
										.parseInt(Var_Define.arrayDefineSave.get(defIndex)[4]); paramIndex++) {
									endIndexCalc -= ("|" + paramIndex + "|").length();
									definitionCalc = definitionCalc.replace("|" + paramIndex + "|", "");
								}

								defineLineCalc = ccuFileArray.get(i)
										.replaceFirst(Pattern.quote(Var_Define.arrayDefineSave.get(defIndex)[2]), definitionCalc);
								ccuFileArray.set(i, defineLineCalc);
							}

							// Gets the definition back to re-add 'DEF' in front
							if (definitionSave != null) {
								ccuFileArray.set(i,
										definitionSave.substring(0, Var_Define.getDefineIndex(definitionSave)) + ccuFileArray.get(i));
							}

						} else {

							// checks whether it is a TELE or COORDS definition with [ and ]
							if (Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[0]) == 4
									|| Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[0]) == 5) {
								if (defineLineCalc.isEmpty() == false && defineLineCalc.contains("[") && defineLineCalc.contains("]")
										&& defineLineCalc.indexOf("[") < defineLineCalc.indexOf("]")) {
									defineLineCalc = defineLineCalc.substring(defineLineCalc.indexOf("[") + 1,
											defineLineCalc.indexOf("]"));

									if (Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[0]) == 4) {
										switch (defineLineCalc) {
										case "x":
											defineCoordsCalc = 0;
											break;
										case "y":
											defineCoordsCalc = 1;
											break;
										case "z":
											defineCoordsCalc = 2;
											break;
										case "2x":
											defineCoordsCalc = 3;
											break;
										case "2y":
											defineCoordsCalc = 4;
											break;
										case "2z":
											defineCoordsCalc = 5;
											break;
										}
									}

									if (Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[0]) == 5) {
										switch (defineLineCalc) {
										case "x":
											defineCoordsCalc = 0;
											break;
										case "y":
											defineCoordsCalc = 1;
											break;
										case "z":
											defineCoordsCalc = 2;
											break;
										case "ry":
											defineCoordsCalc = 3;
											break;
										case "rx":
											defineCoordsCalc = 4;
											break;
										}
									}

									if (defineCoordsCalc == null) {
										System.out.println("ERROR: Parameter '" + defineLineCalc + "' is incorrect in line '"
												+ ccuFileArray.get(i) + "'");
										System.exit(0);
									}

									// array for coords
									defineParamsCalc = Var_Define.arrayDefineSave.get(defIndex)[3].split(" ");

									// removes anything in between [ and ]
									defineLineCalc = ccuFileArray.get(i).substring(0, ccuFileArray.get(i).indexOf("["))
											+ ccuFileArray.get(i).substring(ccuFileArray.get(i).indexOf("]") + 1);

									// replaces the definition with the specific coordinate
									defineLineCalc = defineLineCalc.replaceFirst(
											Pattern.quote(Var_Define.arrayDefineSave.get(defIndex)[2]),
											defineParamsCalc[defineCoordsCalc]);
									ccuFileArray.set(i, defineLineCalc);

									continue;
								}
							}

							// sets it as is because params aren't an issue
							ccuFileArray.set(i,
									ccuFileArray.get(i).replaceFirst(Pattern.quote(Var_Define.arrayDefineSave.get(defIndex)[2]),
											Var_Define.arrayDefineSave.get(defIndex)[3]));

							// add definition after
							if (definitionSave != null) {
								ccuFileArray.set(i,
										definitionSave.substring(0, Var_Define.getDefineIndex(definitionSave)) + ccuFileArray.get(i));
							}
						}

						// tests for recurring definition

						System.out.println(Var_Define.arrayDefineSave.get(defIndex)[2].length());
						System.out.println(begIndexCalc + " " + endIndexCalc);
						System.out.println(ccuFileArray.get(i));
						System.out.println(ccuFileArray.get(i).substring(begIndexCalc, endIndexCalc) + " MARKER");
						System.out.println("");

						for (String testDefinition : usedDefinitionArray) {
							if (ccuFileArray.get(i).substring(begIndexCalc, endIndexCalc).contains(testDefinition)) {
								System.out.println(Var_Define.arrayDefineSave.get(defIndex)[2]);
								System.out.println(testDefinition);

								System.out.println("ERROR: Recurring definition at line '" + ccuFileArray.get(i)
										+ "' starting with the definition '" + testDefinition + "'");
								System.exit(0);
							}
						}
						
						usedDefinitionArray.add(Var_Define.arrayDefineSave.get(defIndex)[2]);
						break;
					} else {

						// meaning no definition matches up
						if (definitionSave != null) {
							ccuFileArray.set(i, definitionSave);
						}
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
							if (indexCalc < this.ccuFileArray.size()
									&& ccuFileArray.get(indexCalc).substring(0, this.tabNum).length() - ccuFileArray.get(indexCalc)
											.substring(0, this.tabNum).replace("\t", "").length() == this.tabNum) {

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

						case "FUNC":
							Var_Func objFunc = new Var_Func(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objFunc.getArray();
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
				// scoreboard shortcuts
				if (Short_Scoreboard.getCommand(ccuFileArray.get(i), tabNum) != null) {
					ccuFileArray.set(i, Short_Scoreboard.getCommand(ccuFileArray.get(i), tabNum));
				}

				// execute shortcuts
				if (Short_Execute.getCommand(ccuFileArray.get(i), tabNum) != null) {
					ccuFileArray.set(i, Short_Execute.getCommand(ccuFileArray.get(i), tabNum));
				}

				// selector shortcuts
				if (Short_Selector.getCommand(ccuFileArray.get(i), tabNum) != null) {
					ccuFileArray.set(i, Short_Selector.getCommand(ccuFileArray.get(i), tabNum));
				}

				// function shortcuts
				if (FunctionNick.getCommand(ccuFileArray.get(i), tabNum) != null) {
					ccuFileArray.set(i, FunctionNick.getCommand(ccuFileArray.get(i), tabNum));
				}

				// server override
				if (ReadConfig.serverPlugins == true
						&& (ReadConfig.serverOverrideArray == null || ReadConfig.serverOverrideArray[0].equals("")) == false) {
					if (ServerOverride.getCommand(ccuFileArray.get(i), tabNum) != null) {
						ccuFileArray.set(i, ServerOverride.getCommand(ccuFileArray.get(i), tabNum));
					}
				}
			}
		}
		return ccuFileArray;
	}
}
