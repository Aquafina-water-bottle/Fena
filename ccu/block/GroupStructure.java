package ccu.block;

import java.util.ArrayList;

import ccu.command.Cmd_Group;
import ccu.command.Var_Options;

public class GroupStructure {
	/** Test
	 * This class will not return anything, although there will be a public static arraylist of:
	 * String[] Commands
	 * Coordinates[] Coordinates
	 * Int[] Direction
	 * 
	 * and also as a 
	 * Int Group Lines (height)
	 */

	public static ArrayList<String[]> groupCommandsArray = new ArrayList<String[]>();
	public static ArrayList<Coordinates[]> groupCoordsArray = new ArrayList<Coordinates[]>();
	public static ArrayList<String[]> groupDirectionArray = new ArrayList<String[]>();
	public static ArrayList<Boolean[]> groupConditionalArray = new ArrayList<Boolean[]>();
	public static ArrayList<Integer> groupLineArray = new ArrayList<Integer>();
	public static int styleOptionY = 0;
	public static String styleOptionXZ = null;

	/*
	public static final int NORTH = 5;
	public static final int SOUTH = 4;
	public static final int UP = 1;
	public static final int DOWN = 0;
	public static final int SIDEWAYS = 3;
	*/

	public static void getGroupStructures() {

		// Get the option from the VAR_Options class
		try {
			styleOptionY = Integer.valueOf(Var_Options.styleOption.substring(3));
		} catch (NumberFormatException | StringIndexOutOfBoundsException e) {
			System.out.println("ERROR: Incorrect syntax for 'styleOption " + Var_Options.styleOption + "'");
			System.exit(0);
		}

		// Getting the other option
		styleOptionXZ = Var_Options.styleOption.substring(0, 2);

		ArrayList<String> groupCommandsArrayCalc = new ArrayList<String>();
		ArrayList<Coordinates> groupCoordsArrayCalc = new ArrayList<Coordinates>();
		ArrayList<String> groupDirectionArrayCalc = new ArrayList<String>();
		ArrayList<Boolean> groupConditionalArrayCalc = new ArrayList<Boolean>();
		int groupLineCalc = 0;

		int directionMoveXZ;
		int directionMoveY;

		int coordTempX;
		int coordTempY;
		int coordTempZ;

		int cmdLength;
		int cmdLengthCalc;
		int cmdLengthCalc2;

		int condCalc;
		int condNum;
		int condState = 0;
		int j;

		for (int i = 0; i < Cmd_Group.arrayGroupSave.size(); i++) {
			groupCommandsArrayCalc.clear();
			groupCoordsArrayCalc.clear();
			groupDirectionArrayCalc.clear();
			groupConditionalArrayCalc.clear();
			groupLineCalc = 0;

			directionMoveXZ = 1;
			directionMoveY = 1;

			coordTempX = 2;
			coordTempY = 1;
			coordTempZ = 1;

			cmdLength = 2;
			cmdLengthCalc = 1;
			cmdLengthCalc2 = 1;
			j = 0;

			while (j < Cmd_Group.arrayGroupSave.get(i).length - 1) {
				j++;
				// Command: CMD_Group.arrayGroupSave.get(i)[j]

				/* Added to each arrayList
				 * directionMoveXZ and directionMoveY are not direct markers of where
				 * things are supposed to be, but rather states on how the command
				 * blocks are supposed to be positioned
				 */

				// detects 2 different combinations:
				// 1) COND NORM COND
				// 2) NORM NORM COND
				if ( // detects if current block = not cond
				(Cmd_Group.arrayGroupSave.get(i)[j].length() < 9) || (Cmd_Group.arrayGroupSave.get(i)[j].length() >= 9
						&& Cmd_Group.arrayGroupSave.get(i)[j].substring(0, 9).equals("CCU_COND_") == false)) {

					//detects 2nd norm, 3rd cond
					if (((j < Cmd_Group.arrayGroupSave.get(i).length - 1) && ((Cmd_Group.arrayGroupSave.get(i)[j + 1].length() < 9)
							|| (Cmd_Group.arrayGroupSave.get(i)[j + 1].length() >= 9
									&& Cmd_Group.arrayGroupSave.get(i)[j + 1].substring(0, 9).equals("CCU_COND_") == false)))
							&& (j + 2 < Cmd_Group.arrayGroupSave.get(i).length && Cmd_Group.arrayGroupSave.get(i)[j + 2].length() >= 9
									&& Cmd_Group.arrayGroupSave.get(i)[j + 2].substring(0, 9).equals("CCU_COND_"))) {
						condState = 1;
					}

					// detects -1 cond, 1 cond
					if ((j - 1 < Cmd_Group.arrayGroupSave.get(i).length && Cmd_Group.arrayGroupSave.get(i)[j - 1].length() >= 9
							&& Cmd_Group.arrayGroupSave.get(i)[j - 1].substring(0, 9).equals("CCU_COND_"))
							&& (j + 1 < Cmd_Group.arrayGroupSave.get(i).length && Cmd_Group.arrayGroupSave.get(i)[j + 1].length() >= 9
									&& Cmd_Group.arrayGroupSave.get(i)[j + 1].substring(0, 9).equals("CCU_COND_"))) {
						condState = 2;
					}

				}

				if (condState >= 1) {
					// counts number of conditional command blocks
					condCalc = j + 1;
					condNum = 0;
					while (true) {
						condCalc++;
						if (condCalc < Cmd_Group.arrayGroupSave.get(i).length
								&& Cmd_Group.arrayGroupSave.get(i)[condCalc].length() >= 9
								&& Cmd_Group.arrayGroupSave.get(i)[condCalc].substring(0, 9).equals("CCU_COND_")) {
							condNum++;
						} else {
							break;
						}
					}
					// System.out.println("future cond: " + condNum + " | " + cmdLength + " | " + condState);

					// depending on what state this is in
					if (condState == 1) {
						if (cmdLength % 16 <= 7) {
							if (14 - (cmdLength % 16) >= condNum) {
								// Stay with the normal layout
								condState = 0;
							} else {
								System.out.println("ERROR: Conditional commands starting at line '"
										+ Cmd_Group.arrayGroupSave.get(i)[j + 2].substring(9) + "' is too long of a line");
								System.exit(0);
							}
						}

						// skips command spaces by setting cmdLengthCalc (and maybe) cmdLengthCalc2 to 0 to force it to move up 1
						if (cmdLength % 16 > 7) {
							if (14 - (cmdLength % 16) >= condNum) {
								// Stay with normal layout
								condState = 0;
							} else {
								if ((cmdLength % 16) - 2 >= condNum) {
									// Bumps up
									cmdLengthCalc = 0;
									directionMoveXZ *= -1;
									if (cmdLengthCalc2 >= (16 * styleOptionY) - 16) {
										cmdLengthCalc2 = 0;
									}
								} else {
									System.out.println("ERROR: Conditional commands starting at line '"
											+ Cmd_Group.arrayGroupSave.get(i)[j + 2].substring(9) + "' is too long");
									System.exit(0);
								}
							}
						}
					}

					// condState as 2
					if (condState == 2) {
						if (cmdLength % 16 <= 8 && cmdLength % 16 >= 1) {
							if (14 - (cmdLength % 16) >= condNum) {
								// Stay with normal layout
								condState = 0;
							} else {
								System.out.println("ERROR: Conditional commands starting at line '"
										+ Cmd_Group.arrayGroupSave.get(i)[j + 1].substring(9) + "' is too long");
								System.exit(0);
							}
						}

						if (cmdLength % 16 > 8 || cmdLength % 16 == 0) {
							if ((14 - (cmdLength % 16)) >= condNum && (cmdLength % 16) != 0) {
								// Stay with normal layout
								condState = 0;
							} else {
								if ((cmdLength % 16) - 2 >= condNum || (cmdLength % 16) == 0) {
									groupCommandsArrayCalc.add("");
									groupConditionalArrayCalc.add(false);
									Coordinates coordObj = new Coordinates(coordTempX, coordTempY, coordTempZ);
									groupCoordsArrayCalc.add(coordObj);
									if (cmdLength % 16 != 0) {
										directionMoveXZ *= -1;
									}

									cmdLengthCalc = 0;
									if (cmdLengthCalc2 >= (16 * styleOptionY) - 16) {
										cmdLengthCalc2 = 0;
									}

									if (cmdLengthCalc == 0) {
										groupLineCalc++;
										if (cmdLengthCalc2 == 0) {
											groupDirectionArrayCalc.add("SIDEWAYS");
											coordTempZ++;
										} else {
											if (directionMoveY == 1) {
												groupDirectionArrayCalc.add("UP");
												coordTempY++;
											}
											if (directionMoveY == -1) {
												groupDirectionArrayCalc.add("DOWN");
												coordTempY--;
											}
										}
									}

									cmdLength = cmdLength + ((16 - (cmdLength % 16)) * 2) + 1;
									cmdLengthCalc = 1;
									cmdLengthCalc2 = 1;
								}
							}
						}

					}

				}

				// Add cmd while removing 'CCU_COND_'
				if (Cmd_Group.arrayGroupSave.get(i)[j].length() >= 9
						&& Cmd_Group.arrayGroupSave.get(i)[j].substring(0, 9).equals("CCU_COND_")) {
					groupCommandsArrayCalc.add(Cmd_Group.arrayGroupSave.get(i)[j].substring(9));
					groupConditionalArrayCalc.add(true);
				} else {
					groupCommandsArrayCalc.add(Cmd_Group.arrayGroupSave.get(i)[j]);
					groupConditionalArrayCalc.add(false);
				}

				// Add coords
				Coordinates coordObj = new Coordinates(coordTempX, coordTempY, coordTempZ);
				groupCoordsArrayCalc.add(coordObj);

				if (cmdLengthCalc != 0) {
					if (directionMoveXZ == 1) {
						groupDirectionArrayCalc.add("NORTH");
						coordTempX++;
					}
					if (directionMoveXZ == -1) {
						groupDirectionArrayCalc.add("SOUTH");
						coordTempX--;
					}
				}

				if (cmdLengthCalc == 0) {

					// only adds to the line if 
					if (j != Cmd_Group.arrayGroupSave.get(i).length - 1) {
						groupLineCalc++;
					}

					if (cmdLengthCalc2 == 0) {
						groupDirectionArrayCalc.add("SIDEWAYS");
						coordTempZ++;
					} else {
						if (directionMoveY == 1) {
							groupDirectionArrayCalc.add("UP");
							coordTempY++;
						}
						if (directionMoveY == -1) {
							groupDirectionArrayCalc.add("DOWN");
							coordTempY--;
						}
					}
				}

				// Adds to cmdLength because of conditional command blocks
				if (condState == 1) {
					condState = 0;
					if (cmdLength % 16 > 7) {
						cmdLength = cmdLength + ((16 - (cmdLength % 16)) * 2);
					}
				}

				// Calculating the direction of the next block
				cmdLength++;
				cmdLengthCalc = cmdLength % 16;
				cmdLengthCalc2 = cmdLength % (16 * styleOptionY);

				if (cmdLengthCalc == 0) {
					directionMoveXZ *= -1;
				}
				if (cmdLengthCalc2 == 0) {
					directionMoveY *= -1;
				}

				/*
				System.out.println(groupCommandsArrayCalc.get(j - 1) + " | " + coordObj.getString() + " | "
						+ groupDirectionArrayCalc.get(j - 1) + " | " + groupConditionalArrayCalc.get(j - 1) + " | "
						+ (cmdLength - 1) + " | " + (groupLineCalc + 1));
				*/
			}

			// adding everything to the public static arrays
			String[] groupCommandsOriginalCalc = new String[groupCommandsArrayCalc.size()];
			Coordinates[] groupCoordsOriginalArray = new Coordinates[groupCoordsArrayCalc.size()];
			String[] groupDirectionOriginalArray = new String[groupDirectionArrayCalc.size()];
			Boolean[] groupConditionalOriginalArray = new Boolean[groupConditionalArrayCalc.size()];

			for (int getArray = 0; getArray < groupCommandsArrayCalc.size(); getArray++) {
				groupCommandsOriginalCalc[getArray] = groupCommandsArrayCalc.get(getArray);
			}
			groupCommandsArray.add(groupCommandsOriginalCalc);

			for (int getArray = 0; getArray < groupCoordsArrayCalc.size(); getArray++) {
				groupCoordsOriginalArray[getArray] = groupCoordsArrayCalc.get(getArray);
			}
			groupCoordsArray.add(groupCoordsOriginalArray);

			for (int getArray = 0; getArray < groupDirectionArrayCalc.size(); getArray++) {
				groupDirectionOriginalArray[getArray] = groupDirectionArrayCalc.get(getArray);
			}
			groupDirectionArray.add(groupDirectionOriginalArray);

			for (int getArray = 0; getArray < groupConditionalArrayCalc.size(); getArray++) {
				groupConditionalOriginalArray[getArray] = groupConditionalArrayCalc.get(getArray);
			}
			groupConditionalArray.add(groupConditionalOriginalArray);

			groupLineArray.add(groupLineCalc + 1);

			/*groupCommandsArrayCalc.clear();
			groupCoordsArrayCalc.clear();
			groupDirectionArrayCalc.clear();
			groupConditionalArrayCalc.clear();
			groupLineCalc = 0;
			*/

			/* public static ArrayList<String[]> groupCommandsArray = new ArrayList<String[]>();
			public static ArrayList<Coordinates[]> groupCoordsArray = new ArrayList<Coordinates[]>();
			public static ArrayList<Integer[]> groupDirectionArray = new ArrayList<Integer[]>();
			public static ArrayList<Boolean[]> groupConditionalArray = new ArrayList<Boolean[]>();
			public static ArrayList<Integer> groupLineArray = new ArrayList<Integer>();
			*/

		}
	}
}
