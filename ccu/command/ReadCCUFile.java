package ccu.command;

import java.io.File;
import java.util.ArrayList;

import ccu.general.GeneralFile;

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
		this.ccuFileArray = GeneralFile.parseCCU(ccuFile.getFileArray());
		// .replaceAll("\\s+$", "")
	}

	public ReadCCUFile(ArrayList<String> arrayName, int tabNumGet) {
		this.ccuFileArray = arrayName;
		this.tabNum = tabNumGet;
	}

	// @formatter:off
	public static final String[] statementArray = {
			"MFUNC",
			"GROUP",
			"DEF",
			"FUNC",
			"IMPORT",
			"UNASSIGN",
			"CALL", 
			"ARRAY",
			"SET",
			"SPLIT",
			"OPTIONS",
			"LOOP",
			"IF",
			"ELSE",
			"ELIF",
			"USE",
			"COND",
			"PRINT",
			"EXIT",
			"INITIALIZE",
			"FINALIZE"
			};
	// @formatter:on

	/*
	 *  proposal on how this will work:
	 * each statement will have its own object
	 * reoccuring method for checkCommands()
	 * 
	 * 3 types of statements:
	 * CMD - Holds commands (GROUP, COND, MFUNC)
	 * 		-These always return NULL once ran
	 * CON - Control flow (USE, IF, LOOP)
	 * 		-These normally return statements once ran
	 * VAR - Variables (ARRAY, DEF, FUNC, OBJADD, OBJSET, OBJDEL, TEAMADD, TEAMSET, TEAMDEL, OPTIONS)
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
		boolean resetArray = false;
		boolean singleLineStatement = false;
		boolean resetIndexCalc = false;
		boolean getStatement = false;
		Boolean checkElse = null;

		ArrayList<String> getCalcArray = new ArrayList<String>();
		ArrayList<String> encapsulateArray = new ArrayList<String>();
		ArrayList<String> subListTopArray = new ArrayList<String>();
		ArrayList<String> subListBottomArray = new ArrayList<String>();

		// Implements any defines, functions, arrays here with the only exceptions being / at the beginning and inside definitions
		// ResetIndex and break from the loop if defines / functions / arrays / imports are found

		// if the define is within it, and the tabnum is less than or equal to define tab num

		int i = -1;
		while (i < this.ccuFileArray.size()) {

			checkElse = null;

			// Resets getStatement
			getStatement = false;

			// Resets index as resetting it at the bottom did not work
			i++;

			// makes sure stuff doesn't happen
			if (this.ccuFileArray.size() - 1 < i) {
				if (i != 0 && (this.ccuFileArray.get(i - 1).trim().equals("CCU_ReturnFalse")
						|| this.ccuFileArray.get(i - 1).trim().equals("CCU_ReturnTrue"))) {
					this.ccuFileArray.remove(i - 1);
				}
				break;
			}

			// If the previous line is "CCU_ReturnFalse"
			if (i > 0) {
				String checkElseString = this.ccuFileArray.get(i - 1).trim();
				if (checkElseString.equals("CCU_ReturnFalse")) {
					checkElse = true;
					this.ccuFileArray.remove(i - 1);
					i--;
				}
				if (checkElseString.equals("CCU_ReturnTrue")) {
					checkElse = false;
					this.ccuFileArray.remove(i - 1);
					i--;
				}
			}

			ccuFileArray.set(i, Var_Define.calcDefine(ccuFileArray.get(i), this.tabNum, ccuFileArray.get(i)));

			// iterates through all functions
			// starts at the negative end to prioritize the more tabulated function
			// this is essentially to create the "CALL {Func_Name}" from the Func_Name itself
			for (int funcIndex = Var_Func.arrayFuncNameSave.size() - 1; funcIndex >= 0; funcIndex--) {
				if (ccuFileArray.get(i).endsWith(")") && ccuFileArray.get(i).contains("(")) {
					if (ccuFileArray.get(i).substring(0, ccuFileArray.get(i).indexOf("(")).trim()
							.equals(Var_Func.arrayFuncNameSave.get(funcIndex)[2])) {

						Var_Call objCall = new Var_Call(ccuFileArray.get(i), this.tabNum);
						ccuFileArray.set(i, objCall.getFuncCall());
						break;
					}
				} else {
					if (ccuFileArray.get(i).trim().equals(Var_Func.arrayFuncNameSave.get(funcIndex)[2])) {
						Var_Call objCall = new Var_Call(ccuFileArray.get(i), this.tabNum);
						ccuFileArray.set(i, objCall.getFuncCall());
						break;
					}
				}
			}

			for (String statement : statementArray) {
				singleLineStatement = false;

				// detects whether it is a proper statement
				if (ccuFileArray.get(i).length() >= (statement.length() + this.tabNum)
						&& ccuFileArray.get(i).substring(this.tabNum, statement.length() + this.tabNum).equals(statement)) {

					// gets statement
					String statementTest = ccuFileArray.get(i).substring(this.tabNum, statement.length() + this.tabNum);
					// Will gather DEF, IMPORT, TEAMREV, OBJREV in this area
					// This is to get the array for said statement

					switch (statementTest) {
					case "DEF":
						Var_Define objDefine = new Var_Define(ccuFileArray.get(i), this.tabNum);
						getCalcArray = objDefine.getArray();
						resetArray = true;
						singleLineStatement = true;
						break;

					case "CALL":
						Var_Call objCall = new Var_Call(ccuFileArray.get(i), this.tabNum);
						getCalcArray = objCall.getArray();
						resetArray = true;
						singleLineStatement = true;
						break;

					case "SET":
						Var_Set objSet = new Var_Set(ccuFileArray.get(i), this.tabNum);
						getCalcArray = objSet.getArray();
						resetArray = true;
						singleLineStatement = true;
						break;

					case "IMPORT":
						Var_Import objImport = new Var_Import(ccuFileArray.get(i), this.tabNum);
						getCalcArray = objImport.getArray();
						resetArray = true;
						singleLineStatement = true;
						break;

					case "UNASSIGN":
						Var_Unassign objUnassign = new Var_Unassign(ccuFileArray.get(i), this.tabNum);
						getCalcArray = objUnassign.getArray();
						resetArray = true;
						singleLineStatement = true;
						break;

					case "SPLIT":
						Var_Split objSplit = new Var_Split(ccuFileArray.get(i), this.tabNum);
						getCalcArray = objSplit.getArray();
						resetArray = true;
						singleLineStatement = true;
						break;
						
					case "PRINT":
						String printString = ccuFileArray.get(i).replaceFirst("PRINT", "");
						System.out.println(printString.replaceAll("^\\s+", ""));
						getCalcArray = null;
						resetArray = true;
						singleLineStatement = true;
						break;

					case "EXIT":
						String exitString = ccuFileArray.get(i).replaceFirst("EXIT", "");
						System.out.println("EXIT:\t" + exitString.replaceAll("^\\s+", ""));
						System.exit(0);
						break;
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
							if (i > 0) {
								subListTopArray = new ArrayList<String>(this.ccuFileArray.subList(0, i));
								// System.out.println(subListTopArray);
							} else {
								subListTopArray.clear();
							}
							subListBottomArray = new ArrayList<String>(this.ccuFileArray.subList(i + 1, this.ccuFileArray.size()));
						}

						/*
						System.out.println(subListTopArray);
						System.out.println(encapsulateArray);
						System.out.println(subListBottomArray);
						System.out.println("");
						*/

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
							Cmd_Cond objCond = new Cmd_Cond(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objCond.getArray();
							resetArray = true;
							break;

						case "FUNC":
							Var_Func objFunc = new Var_Func(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objFunc.getArray();
							resetArray = true;
							break;

						case "LOOP":
							Con_Loop objLoop = new Con_Loop(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objLoop.getArray();
							resetArray = true;
							break;

						case "IF":
							Con_If objIf = new Con_If(encapsulateArray, this.tabNum, ccuFileArray.get(i), true);
							getCalcArray = objIf.getArray();
							resetArray = true;
							break;

						case "ARRAY":
							Var_Array objArray = new Var_Array(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objArray.getArray();
							resetArray = true;
							break;

						case "ELSE":
							Con_Else objElse = new Con_Else(encapsulateArray, this.tabNum, ccuFileArray.get(i), checkElse);
							getCalcArray = objElse.getArray();
							resetArray = true;
							break;

						case "ELIF":
							Con_Elif objElif = new Con_Elif(encapsulateArray, this.tabNum, ccuFileArray.get(i), checkElse);
							getCalcArray = objElif.getArray();
							resetArray = true;
							break;

						case "INITIALIZE":
							Cmd_Initialize objInitialize = new Cmd_Initialize(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objInitialize.getArray();
							resetArray = true;
							break;

						case "FINALIZE":
							Cmd_Finalize objFinalize = new Cmd_Finalize(encapsulateArray, this.tabNum, ccuFileArray.get(i));
							getCalcArray = objFinalize.getArray();
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

					if (subListTopArray != null) {
						ccuFileArray.addAll(subListTopArray);
					}
					if (getCalcArray != null) {
						ccuFileArray.addAll(getCalcArray);
					}
					if (subListBottomArray != null) {
						ccuFileArray.addAll(subListBottomArray);
					}

					// only resets when the the statement isn't a single line
					if (singleLineStatement == false) {

						// reset all definitions that don't work with the decreasing tab numbers
						for (int defIndex = 0; defIndex < Var_Define.arrayDefineSave.size(); defIndex++) {
							if (resetIndexCalc == true) {
								resetIndexCalc = false;
								defIndex = 0;
							}
							if (this.tabNum == Integer.parseInt(Var_Define.arrayDefineSave.get(defIndex)[1])) {
								resetIndexCalc = true;
								Var_Define.arrayDefineSave.remove(defIndex);
							}
						}

						// reset all functions that don't work with the decreasing tab numbers
						for (int funcIndex = 0; funcIndex < Var_Func.arrayFuncNameSave.size(); funcIndex++) {
							if (resetIndexCalc == true) {
								resetIndexCalc = false;
								funcIndex = 0;
							}
							if (this.tabNum == Integer.parseInt(Var_Func.arrayFuncNameSave.get(funcIndex)[1])) {
								resetIndexCalc = true;
								Var_Func.arrayFuncSave.remove(funcIndex);
								Var_Func.arrayFuncNameSave.remove(funcIndex);
							}
						}

						// reset all arrays that don't work with the decreasing tab numbers
						for (int arrayIndex = 0; arrayIndex < Var_Array.singleArrayNameSave.size(); arrayIndex++) {
							if (resetIndexCalc == true) {
								resetIndexCalc = false;
								arrayIndex = 0;
							}
							if (this.tabNum == Integer.parseInt(Var_Array.singleArrayNameSave.get(arrayIndex)[1])) {
								resetIndexCalc = true;
								Var_Array.singleArraySave.remove(arrayIndex);
								Var_Array.singleArrayNameSave.remove(arrayIndex);
							}
						}
						for (int arrayIndex = 0; arrayIndex < Var_Array.doubleArrayNameSave.size(); arrayIndex++) {
							if (resetIndexCalc == true) {
								resetIndexCalc = false;
								arrayIndex = 0;
							}
							if (this.tabNum == Integer.parseInt(Var_Array.doubleArrayNameSave.get(arrayIndex)[1])) {
								resetIndexCalc = true;
								Var_Array.doubleArraySave.remove(arrayIndex);
								Var_Array.doubleArrayNameSave.remove(arrayIndex);
							}
						}

						indexCalc = 0;
						this.tabNum--;
					}

					// general reset
					resetArray = false;
					i--;
					break;
				}
			}

			if (getStatement == false) {
				// includes PARSE, CALC, SIN, COS, TAN here

			}
		}
		return ccuFileArray;
	}
}
