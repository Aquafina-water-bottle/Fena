package ccu.block;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;

import ccu.command.Cmd_Group;
import ccu.command.Cmd_MFunc;
import ccu.command.Var_Import;
import ccu.command.Var_Options;
import ccu.general.GeneralFile;
import ccu.general.ParamUtils;
import ccu.general.ReadConfig;

public class Box {
	/**
	 * Practically this entire class is horrible ass programming since
	 * idk how else to group together command blocks apart from using
	 * a physical array to arrange them
	 */

	// constructing the array to encapsulate all known groups
	public static Coordinates[] groupNameCoordArray = new Coordinates[Cmd_Group.arrayGroupSave.size()];
	public static Coordinates[] groupNameFillArray = new Coordinates[Cmd_Group.arrayGroupSave.size()];
	public static Coordinates fillCoords1 = new Coordinates();
	public static Coordinates fillCoords2 = new Coordinates();

	// calc array to combine imported arrays
	private static ArrayList<String> importNameCoordArray = new ArrayList<String>();
	private static ArrayList<Coordinates> importCoordArray = new ArrayList<Coordinates>();
	private static ArrayList<Coordinates> importFillCoordArray = new ArrayList<Coordinates>();

	private static int[][] removeArrayInt(int[][] blockArrayGet, int getY, int getXZ, int replaceIn, int replaceWith) {
		for (int i = 0; i < getXZ; i++) {
			for (int j = 0; j < getY; j++) {
				if (blockArrayGet[j][i] == replaceIn) {
					blockArrayGet[j][i] = replaceWith;
				}
			}

		}
		return blockArrayGet;
	}

	/*
	private static void printArray(int[][] blockArray, int xz, int y) {
		if (xz != 0) {
			System.out.println("");
			for (int asdf = 0; asdf < xz; asdf++) {
				for (int asfd = 0; asfd < y; asfd++) {
					if (blockArray[asfd][asdf] == 1) {
						System.out.print("# ");
					} else {
						if (blockArray[asfd][asdf] == 2 || blockArray[asfd][asdf] == 0) {
							System.out.print("- ");
						} else {
							System.out.print("E ");
						}
					}
				}
				System.out.println("");
			}
			System.out.println("");
		}
	}*/

	private static int[][] surroundingArrayInt(int[][] blockArrayGet, int getY, int getXZ, int detectInt, int surroundInt) {
		/** When it detects number 'detectInt', it replaces the surrounding numbers with 'surroundInt'
		 * - assuming the surrounding number is 0
		 */
		int[] offsetArray = {0, 0};

		for (int i = 0; i < getXZ; i++) {
			for (int j = 0; j < getY; j++) {
				// System.out.println(j + " " + i);
				if (blockArrayGet[j][i] == detectInt) {

					offsetArray[0] = 1;
					offsetArray[1] = -1;
					try {
						if (blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] == 0) {
							blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] = surroundInt;
						}
					} catch (Exception e) {
					}

					offsetArray[1] = 0;
					try {
						if (blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] == 0) {
							blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] = surroundInt;
						}
					} catch (Exception e) {
					}

					offsetArray[1] = 1;
					try {
						if (blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] == 0) {
							blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] = surroundInt;
						}
					} catch (Exception e) {
					}

					offsetArray[0] = 0;
					offsetArray[1] = -1;
					try {
						if (blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] == 0) {
							blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] = surroundInt;
						}
					} catch (Exception e) {
					}

					offsetArray[1] = 1;
					try {
						if (blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] == 0) {
							blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] = surroundInt;
						}
					} catch (Exception e) {
					}

					offsetArray[0] = -1;
					offsetArray[1] = -1;
					try {
						if (blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] == 0) {
							blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] = surroundInt;
						}
					} catch (Exception e) {
					}

					offsetArray[1] = 0;
					try {
						if (blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] == 0) {
							blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] = surroundInt;
						}
					} catch (Exception e) {
					}

					offsetArray[1] = 1;
					try {
						if (blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] == 0) {
							blockArrayGet[j + offsetArray[0]][i + offsetArray[1]] = surroundInt;
						}
					} catch (Exception e) {
					}

				}
			}

		}
		return blockArrayGet;
	}

	public static void getBox() {
		// for (int i = 0; i < CMD_Group.arrayGroupSave.size(); i++) {
		// Actual length
		// groupSizeArray[i] = CMD_Group.arrayGroupSave.get(i).length - 1;
		// }

		// Approximation for array creation
		int arrayApprox = (int) Math
				.ceil(((GroupStructure.groupLineArray.stream().mapToInt(Integer::intValue).sum() * 5) / GroupStructure.styleOptionY));

		if (arrayApprox == 0 && GroupStructure.groupLineArray.isEmpty() == false && GroupStructure.groupLineArray.get(0) > 0) {
			arrayApprox = 1;
		}
		// GroupStructure.groupLineArray.stream().mapToInt(Integer::intValue).sum();

		// Creating the array
		int[][] blockArray = new int[GroupStructure.styleOptionY][arrayApprox];

		for (int i = 0; i < GroupStructure.styleOptionY; i++) {
			Arrays.fill(blockArray[i], 0);
		}

		// Gets array
		int coordsSaveY = 0;
		int coordsSaveXZ = 0;
		int coordsCalcY = 0;
		int coordsCalcXZ = 0;
		int lengthCalc = 0;
		int directionMoveY = 1;
		int[][] blockArrayCalc;
		boolean foundCmd = false;
		int fillCoordsCalc = 0;
		int fillCoordsCalcY = 0;

		for (int i = 0; i < GroupStructure.groupLineArray.size(); i++) {
			coordsSaveY = 0;
			coordsSaveXZ = 0;
			coordsCalcY = 0;
			coordsCalcXZ = 0;
			lengthCalc = 0;
			directionMoveY = 1;
			foundCmd = false;

			for (int xz = 0; xz < arrayApprox; xz++) {
				for (int y = 0; y < GroupStructure.styleOptionY; y++) {
					// tests if the block at the array is 0
					if (blockArray[y][xz] == 0) {
						if (lengthCalc == 0) {
							lengthCalc = 1;
							// saves the coords for testing purposes later
							coordsSaveY = y;
							coordsSaveXZ = xz;
							coordsCalcY = y;
							coordsCalcXZ = xz;

							// copies array for calcs
							blockArrayCalc = blockArray.clone();

							// does while loop to test if the position works
							while (true) {
								try {
									if (blockArrayCalc[coordsCalcY][coordsCalcXZ] != 0) {
										lengthCalc = 0;
										blockArray = removeArrayInt(blockArrayCalc.clone(), GroupStructure.styleOptionY, arrayApprox,
												10, 0);
										break;
									}
									blockArrayCalc[coordsCalcY][coordsCalcXZ] = 10;
								} catch (ArrayIndexOutOfBoundsException e) {
									System.out.println(
											"ERROR: The developer goofed up when trying to make the box (REPORT IMMEDIATELY)");

									System.out.println(coordsCalcY + " | " + coordsCalcXZ);
									System.out.println(GroupStructure.styleOptionY + " | " + arrayApprox);

									System.exit(0);
								}

								// success
								if (lengthCalc == GroupStructure.groupLineArray.get(i)) {
									blockArrayCalc = surroundingArrayInt(blockArrayCalc.clone(), GroupStructure.styleOptionY,
											arrayApprox, 10, 2);

									// printArray(blockArray, arrayApprox, GroupStructure.styleOptionY);
									// System.out.println("ASDF");

									blockArray = removeArrayInt(blockArrayCalc.clone(), GroupStructure.styleOptionY, arrayApprox, 10,
											1);

									for (int j = 0; j < GroupStructure.groupCoordsArray.get(i).length; j++) {
										GroupStructure.groupCoordsArray.get(i)[j] = GroupStructure.groupCoordsArray.get(i)[j]
												.addCoordinates(0, coordsSaveY, coordsSaveXZ).switchDirection()
												.addCoordinates(Var_Options.coordsOption);
									}

									// Get block coords
									Coordinates groupNameCoordsObj = new Coordinates(0, coordsSaveY, coordsSaveXZ);
									groupNameCoordArray[i] = groupNameCoordsObj.addCoordinates(1, 1, 1).switchDirection()
											.addCoordinates(Var_Options.coordsOption);

									// Get secondary fill block coords (mostly for removing the group)
									groupNameCoordsObj = new Coordinates(0, coordsSaveY, coordsSaveXZ);
									if (GroupStructure.groupLineArray.get(i) <= 16) {
										groupNameFillArray[i] = groupNameCoordsObj
												.addCoordinates(16, GroupStructure.groupLineArray.get(i), 1).switchDirection()
												.addCoordinates(Var_Options.coordsOption);
									} else {
										groupNameFillArray[i] = groupNameCoordsObj
												.addCoordinates(16, 16,
														(int) (Math.ceil(GroupStructure.groupLineArray.get(i) / 16) + 1))
												.switchDirection().addCoordinates(Var_Options.coordsOption);
									}

									foundCmd = true;
									break;
								}

								if (foundCmd == true) {
									break;
								}

								lengthCalc++;

								// adds/removes one from y coord
								if (directionMoveY == 1) {
									coordsCalcY++;
								} else {
									if (directionMoveY == -1)
										coordsCalcY--;
								}

								// tests if y length is correct: negative direction
								if (coordsCalcY == -1) {
									if (lengthCalc % GroupStructure.styleOptionY == 1) {
										directionMoveY = 1;
										coordsCalcY++;
										coordsCalcXZ++;
									} else {
										lengthCalc = 0;
										blockArray = removeArrayInt(blockArrayCalc.clone(), GroupStructure.styleOptionY, arrayApprox,
												10, 0);
										break;
									}
								}

								// tests of y length is correct: positive direction
								if (coordsCalcY == GroupStructure.styleOptionY) {
									if (lengthCalc % GroupStructure.styleOptionY == 1) {
										directionMoveY = -1;
										coordsCalcY--;
										coordsCalcXZ++;
									} else {
										lengthCalc = 0;
										blockArray = removeArrayInt(blockArrayCalc.clone(), GroupStructure.styleOptionY, arrayApprox,
												10, 0);
										break;
									}
								}
							}
						}
					}
				}
				if (foundCmd == true) {
					break;
				}
			}
		}

		boolean foundEmptyLineXZ = false;
		boolean foundEmptyLineY = false;

		// get 2nd fill xz length
		if (arrayApprox != 0) {
			int fillCoordsArrayCalc = 0;

			for (int xz = 0; xz < arrayApprox; xz++) {
				fillCoordsArrayCalc = 0;

				for (int y = 0; y < GroupStructure.styleOptionY; y++) {
					fillCoordsArrayCalc += blockArray[y][xz];
					if (fillCoordsArrayCalc > 0) {
						// fillCoordsCalc is always 1 line ahead because it counts "2"s
						fillCoordsCalc++;
						break;
					}
				}

				if (fillCoordsArrayCalc == 0) {
					foundEmptyLineXZ = true;
					break;
				}
			}

			// gets 2nd fill y length
			for (int y = 0; y < GroupStructure.styleOptionY; y++) {
				fillCoordsArrayCalc = 0;

				for (int xz = 0; xz < arrayApprox; xz++) {
					fillCoordsArrayCalc += blockArray[y][xz];
					if (fillCoordsArrayCalc > 0) {
						// fillCoordsCalc is always 1 line ahead because it counts "2"s
						fillCoordsCalcY++;
						break;
					}
				}

				if (fillCoordsArrayCalc == 0) {
					foundEmptyLineY = true;
					break;
				}
			}
		}

		// System.out.println(fillCoordsCalcY + " | " + fillCoordsCalc);
		// printArray(blockArray, fillCoordsCalc, fillCoordsCalcY);

		if (foundEmptyLineXZ == true) {
			fillCoordsCalc--;
		}

		if (foundEmptyLineY == true) {
			fillCoordsCalcY--;
		}

		fillCoords1.switchDirection().addCoordinates(Var_Options.coordsOption);
		fillCoords2.addCoordinates(17, fillCoordsCalcY + 1, fillCoordsCalc + 1).switchDirection()
				.addCoordinates(Var_Options.coordsOption);
	}

	private static void replaceCoordsSingle(ArrayList<String> arrayList, boolean isFunction, int startInt) {
		/** Any setblock/fill [groupname] will have their coords placed here
		 * eg. fill Grp_asdf air 0 --> "Grp_asdf" will be replaced with coords
		 */
		boolean validFunctionCoords = true;
		boolean foundCoords = false;

		if (isFunction && Var_Options.coordsOption.isRelative()) {
			validFunctionCoords = false;
		}

		// get group command array
		for (int i = 0; i < arrayList.size(); i++) {

			// iterating through group names
			// keep in mind Grp_Name[x, 5 + y, z] and {"value":"fill Grp_Name air 0"}
			do {
				// needs the do {} while bit because of 'fill'
				/*
				importNameCoordArray.add(Cmd_Group.arrayGroupSave.get(i)[0]);
				importCoordArray.add(groupNameCoordArray[i]);
				importFillCoordArray.add(groupNameFillArray[i]);
				 */

				for (int nameIndex = 0; nameIndex < importNameCoordArray.size(); nameIndex++) {

					String begStringCalc = null;
					String coordsCalc = null;
					String paramsCalc = null;
					String[] getArrayCalc = null;

					Integer begIndex = null;
					Integer endIndex = null;

					foundCoords = false;

					if (arrayList.get(i).contains(importNameCoordArray.get(nameIndex))) {

						String testGroupName = arrayList.get(i).substring(
								arrayList.get(i).indexOf(importNameCoordArray.get(nameIndex)) - 1,
								arrayList.get(i).indexOf(importNameCoordArray.get(nameIndex))
										+ importNameCoordArray.get(nameIndex).length() + 1);

						boolean properGroupName = false;

						// if it's a direct group name
						if (testGroupName.trim().equals(importNameCoordArray.get(nameIndex))) {
							properGroupName = true;
						}

						// if the group name has [ after it
						if (testGroupName.endsWith("[") && testGroupName.trim().substring(0, testGroupName.trim().length() - 1)
								.equals(importNameCoordArray.get(nameIndex))) {
							properGroupName = true;
						}

						if (properGroupName) {
							/*
							String testSetblockAsdf = testSetblock.substring(testSetblock.indexOf("Grp_GeneralOptionsTFClock") - 1,
							testSetblock.indexOf("Grp_GeneralOptionsTFClock") + "Grp_GeneralOptionsTFClock".length() + 1);
							 */
							foundCoords = true;

							if (validFunctionCoords == false) {
								System.out.println("ERROR: '" + importNameCoordArray.get(nameIndex) + "' in line '" + arrayList.get(i)
										+ "' cannot be parsed because it is a within a function and coordsOption is relative");
								System.exit(0);
							}

							begIndex = arrayList.get(i).indexOf(importNameCoordArray.get(nameIndex));
							endIndex = arrayList.get(i).indexOf(importNameCoordArray.get(nameIndex))
									+ importNameCoordArray.get(nameIndex).length();

							// gets everything before the coords
							begStringCalc = arrayList.get(i).substring(0, begIndex);

							// gets parameters and anything after the coords
							paramsCalc = arrayList.get(i).substring(endIndex);

							coordsCalc = importCoordArray.get(nameIndex).getString();
							if (begStringCalc.endsWith("fill ") || begStringCalc.endsWith("clone ")) {
								coordsCalc += " " + importFillCoordArray.get(nameIndex).getString();
							}
						}
					}

					if (foundCoords) {

						if (paramsCalc.startsWith("[")) {
							getArrayCalc = ParamUtils.parseCoordinates(paramsCalc, coordsCalc, 4, arrayList.get(i));
							coordsCalc = getArrayCalc[0];
							paramsCalc = getArrayCalc[1];
						}

						arrayList.set(i, begStringCalc + coordsCalc + paramsCalc);
						break;
					}

					String selfReference = "GSELF";
					if (arrayList.get(i).contains(selfReference)) {
						foundCoords = true;

						if (validFunctionCoords == false) {
							System.out.println("ERROR: '" + selfReference + "' in line '" + arrayList.get(i)
									+ "' cannot be parsed because it is a within a function and coordsOption is relative");
							System.exit(0);
						}

						begIndex = arrayList.get(i).indexOf(selfReference);
						endIndex = arrayList.get(i).indexOf(selfReference) + selfReference.length();

						// gets everything before the coords
						begStringCalc = arrayList.get(i).substring(0, begIndex);

						// gets parameters and anything after the coords
						paramsCalc = arrayList.get(i).substring(endIndex);

						coordsCalc = groupNameCoordArray[i].getString();
						if (begStringCalc.endsWith("fill ") || begStringCalc.endsWith("clone ")) {
							coordsCalc += " " + importFillCoordArray.get(i).getString();
						}
					}

					if (foundCoords) {

						if (paramsCalc.startsWith("[")) {
							getArrayCalc = ParamUtils.parseCoordinates(paramsCalc, coordsCalc, 4, arrayList.get(i));
							coordsCalc = getArrayCalc[0];
							paramsCalc = getArrayCalc[1];
						}

						arrayList.set(i, begStringCalc + coordsCalc + paramsCalc);
						break;
					}
				}
			} while (foundCoords);
		}
	}

	private static void replaceCoords(ArrayList<String[]> arrayList, boolean isFunction, int startInt) {
		/** Any setblock/fill [groupname] will have their coords placed here
		 * eg. fill Grp_asdf air 0 --> "Grp_asdf" will be replaced with coords
		 */
		boolean validFunctionCoords = true;
		boolean foundCoords = false;

		if (isFunction && Var_Options.coordsOption.isRelative()) {
			validFunctionCoords = false;
		}

		// get group command array
		for (int i = 0; i < arrayList.size(); i++) {

			// get actual commands
			for (int j = startInt; j < arrayList.get(i).length; j++) {

				// iterating through group names
				// keep in mind Grp_Name[x, 5 + y, z] and {"value":"fill Grp_Name air 0"}
				do {
					// needs the do {} while bit because of 'fill'
					/*
					importNameCoordArray.add(Cmd_Group.arrayGroupSave.get(i)[0]);
					importCoordArray.add(groupNameCoordArray[i]);
					importFillCoordArray.add(groupNameFillArray[i]);
					 */

					for (int nameIndex = 0; nameIndex < importNameCoordArray.size(); nameIndex++) {

						String begStringCalc = null;
						String coordsCalc = null;
						String paramsCalc = null;
						String[] getArrayCalc = null;

						Integer begIndex = null;
						Integer endIndex = null;

						foundCoords = false;

						if (arrayList.get(i)[j].contains(importNameCoordArray.get(nameIndex))) {

							int begCoordIndex = 0;
							int endCoordIndex = 0;

							// test if you can properly substring it lol
							begCoordIndex = arrayList.get(i)[j].indexOf(importNameCoordArray.get(nameIndex)) - 1;
							if (begCoordIndex < 0) {
								begCoordIndex = 0;
							}

							endCoordIndex = arrayList.get(i)[j].indexOf(importNameCoordArray.get(nameIndex))
									+ importNameCoordArray.get(nameIndex).length() + 1;

							if (endCoordIndex > arrayList.get(i)[j].length() - 1) {
								endCoordIndex = arrayList.get(i)[j].length();
							}

							String testGroupName = arrayList.get(i)[j].substring(begCoordIndex, endCoordIndex);
							boolean properGroupName = false;

							// if it's a direct group name
							if (testGroupName.trim().equals(importNameCoordArray.get(nameIndex))) {
								properGroupName = true;
							}

							// if the group name has [ after it
							if (testGroupName.endsWith("[") && testGroupName.trim().substring(0, testGroupName.trim().length() - 1)
									.equals(importNameCoordArray.get(nameIndex))) {
								properGroupName = true;
							}

							if (properGroupName) {
								/*
								String testSetblockAsdf = testSetblock.substring(testSetblock.indexOf("Grp_GeneralOptionsTFClock") - 1,
								testSetblock.indexOf("Grp_GeneralOptionsTFClock") + "Grp_GeneralOptionsTFClock".length() + 1);
								 */
								foundCoords = true;

								if (validFunctionCoords == false) {
									System.out.println("ERROR: '" + importNameCoordArray.get(nameIndex) + "' in line '"
											+ arrayList.get(i)[j]
											+ "' cannot be parsed because it is a within a function and coordsOption is relative");
									System.exit(0);
								}

								begIndex = arrayList.get(i)[j].indexOf(importNameCoordArray.get(nameIndex));
								endIndex = arrayList.get(i)[j].indexOf(importNameCoordArray.get(nameIndex))
										+ importNameCoordArray.get(nameIndex).length();

								// gets everything before the coords
								begStringCalc = arrayList.get(i)[j].substring(0, begIndex);

								// gets parameters and anything after the coords
								paramsCalc = arrayList.get(i)[j].substring(endIndex);

								if (isFunction) {
									coordsCalc = importCoordArray.get(nameIndex).getString();
									if (begStringCalc.endsWith("fill ") || begStringCalc.endsWith("clone ")) {
										coordsCalc += " " + importFillCoordArray.get(nameIndex).getString();
									}
								} else {
									coordsCalc = importCoordArray.get(nameIndex)
											.checkRelative(GroupStructure.groupCoordsArray.get(i)[j]).getString();
									if (begStringCalc.endsWith("fill ") || begStringCalc.endsWith("clone ")) {
										coordsCalc += " " + importFillCoordArray.get(nameIndex)
												.checkRelative(GroupStructure.groupCoordsArray.get(i)[j]).getString();
									}
								}
							}
						}

						if (foundCoords) {

							if (paramsCalc.startsWith("[")) {
								getArrayCalc = ParamUtils.parseCoordinates(paramsCalc, coordsCalc, 4, arrayList.get(i)[j]);
								coordsCalc = getArrayCalc[0];
								paramsCalc = getArrayCalc[1];
							}

							arrayList.get(i)[j] = begStringCalc + coordsCalc + paramsCalc;
							break;
						}

						String selfReference = "GSELF";
						if (arrayList.get(i)[j].contains(selfReference)) {
							foundCoords = true;

							if (validFunctionCoords == false) {
								System.out.println("ERROR: '" + selfReference + "' in line '" + arrayList.get(i)[j]
										+ "' cannot be parsed because it is a within a function and coordsOption is relative");
								System.exit(0);
							}

							begIndex = arrayList.get(i)[j].indexOf(selfReference);
							endIndex = arrayList.get(i)[j].indexOf(selfReference) + selfReference.length();

							// gets everything before the coords
							begStringCalc = arrayList.get(i)[j].substring(0, begIndex);

							// gets parameters and anything after the coords
							paramsCalc = arrayList.get(i)[j].substring(endIndex);

							if (isFunction) {
								coordsCalc = groupNameCoordArray[i].getString();
								if (begStringCalc.endsWith("fill ") || begStringCalc.endsWith("clone ")) {
									coordsCalc += " " + importFillCoordArray.get(i).getString();
								}
							} else {
								coordsCalc = groupNameCoordArray[i].checkRelative(GroupStructure.groupCoordsArray.get(i)[j])
										.getString();
								if (begStringCalc.endsWith("fill ") || begStringCalc.endsWith("clone ")) {
									coordsCalc += " " + groupNameFillArray[i].checkRelative(GroupStructure.groupCoordsArray.get(i)[j])
											.getString();
								}
							}
						}

						if (foundCoords) {

							if (paramsCalc.startsWith("[")) {
								getArrayCalc = ParamUtils.parseCoordinates(paramsCalc, coordsCalc, 4, arrayList.get(i)[j]);
								coordsCalc = getArrayCalc[0];
								paramsCalc = getArrayCalc[1];
							}

							arrayList.get(i)[j] = begStringCalc + coordsCalc + paramsCalc;
							break;
						}
					}
				} while (foundCoords);
			}
		}
	}

	public static void finalizeCoords() {
		/** Get coordinates in commands
		 * TODO: This must also include imported name_dat.txt files
		 * 
		 * Use stringbuilder --> split array, detect whether any match exactly with group name
		 * - detects whether i - 1 is exactly "setblock" or "fill", then do coords accordingly
		 * Remember that imported commands have to be detected, they must be added to the array as FileName.Grp_GeneralScoreboardStart
		 * Also if anything is relative in x, y, z, all become relative and fills relative
		 * 
		 * Gives warning if it is followed up by an execute command if relative
		 * This part DOES NOT account for coords or tp definitions where
		 * 	$CloudCoords$[rx] --> get rot on x axis aka 4th number
		 * that is for the defintions ONLY
		 * */

		String initialFillCommand = null;

		// Gets the name_dat.ccu file as a string to open
		String regFileCalc = ReadConfig.regFilePath.getName().toString();
		regFileCalc = regFileCalc.substring(0, regFileCalc.indexOf(".ccu")) + "_dat.txt";
		File writeDatFile = new File(ReadConfig.regFilePath.getParentFile().toString() + "//" + regFileCalc);

		// Adds to the initialCommands (previous fill air command)
		if (writeDatFile.isFile()) {
			GeneralFile readDatFile = new GeneralFile(writeDatFile);
			ArrayList<String> datFileArray = readDatFile.getFileArray();
			if (datFileArray.size() != 0) {
				initialFillCommand = "fill " + datFileArray.get(0) + " air 0";
				if (GroupStructure.groupCommandsArray.isEmpty() == false) {
					Setblock.initialCommands.add(initialFillCommand);
				}
			}
		}

		// Actually opens the file
		PrintWriter writer = null;
		try {
			writer = new PrintWriter(writeDatFile, "UTF-8");
		} catch (FileNotFoundException | UnsupportedEncodingException e) {
			GeneralFile.dispError(e);
			System.exit(0);
		}

		// Write out initial fill coords if groups exist
		if (GroupStructure.groupCommandsArray.isEmpty() == false) {
			writer.println(fillCoords1.getString() + " " + fillCoords2.getString());
		}

		// Checks if the fill commands are the same
		if ((initialFillCommand == null
				|| initialFillCommand.equals("fill " + fillCoords1.getString() + " " + fillCoords2.getString() + " air 0") == false)
				&& GroupStructure.groupCommandsArray.isEmpty() == false) {

			// Adds to the initialCommands (current fill commands)
			Setblock.initialCommands.add("fill " + fillCoords1.getString() + " " + fillCoords2.getString() + " air 0");
		}

		// Write out coords for each group name
		for (int i = 0; i < Cmd_Group.arrayGroupSave.size(); i++) {
			writer.println(Cmd_Group.arrayGroupSave.get(i)[0] + ";" + groupNameCoordArray[i].getString() + ";"
					+ groupNameFillArray[i].getString());
		}
		// writer.println("\u221a");
		writer.close();

		// Combines existing groups with imported groups
		importNameCoordArray.addAll(Var_Import.datCoordNameArray);
		importCoordArray.addAll(Var_Import.datCoordArray);
		importFillCoordArray.addAll(Var_Import.datCoordFillArray);

		for (int i = 0; i < Cmd_Group.arrayGroupSave.size(); i++) {
			importNameCoordArray.add(Cmd_Group.arrayGroupSave.get(i)[0]);
			importCoordArray.add(groupNameCoordArray[i]);
			importFillCoordArray.add(groupNameFillArray[i]);
		}

		// Replaces the coords for the commands
		replaceCoords(GroupStructure.groupCommandsArray, false, 0);
		replaceCoords(Cmd_MFunc.arrayMFuncSave, true, 1);
		replaceCoordsSingle(Setblock.initialCommands, true, 0);
		replaceCoordsSingle(Setblock.finalCommands, true, 0);
	}
}
