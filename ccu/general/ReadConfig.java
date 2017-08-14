package ccu.general;

import java.io.File;
import java.util.ArrayList;

class TestForError {
	boolean failedTest = false;

	// methods for checking whether the input from the ini file is valid
	void fileCheckError(File fileName, String varPathName) {
		if (fileName == null) {
			System.out.println("ERROR: " + varPathName + " was not found in the .ini file");
			failedTest = true;
		} else {
			if (fileName.exists() == false) {
				System.out.println("ERROR: File " + fileName.toString() + " does not exist");
				failedTest = true;
			} else {
				if (fileName.isFile() == false) {
					System.out.println("ERROR: " + fileName.toString() + " is not a file");
					failedTest = true;
				} else {
					System.out.println("File found: " + fileName.getName());
				}
			}
		}
	}

	void arrayCheckError(String[] arrayName, String textArrayName, boolean softError) {
		// it is fine if array.length = 0 because these techincally aren't
		// stating the array is necessary as well as having "=",
		// but anything after that isn't unless stated by boolean softError
		if (arrayName == null) {
			System.out.println("ERROR: Array " + textArrayName + " does not exist");
			failedTest = true;
		} else {
			if (arrayName[0].equals("")) {
				if (softError == false) {
					System.out.println("ERROR: Array " + textArrayName + " is empty in the .ini file");
					failedTest = true;
				} else {
					System.out.println("WARNING: Array " + textArrayName + " is empty in the .ini file");
				}
			}
			System.out.println("Array found: " + textArrayName);
		}
	}
}

public class ReadConfig {
	public static Integer mcVersion = null;
	public static File regFilePath = null;
	public static File globalFilePath = null;
	public static File globalFunctionFilePath = null;
	public static File importLibraryPath = null;
	public static Boolean preventServerKick = null;
	public static Boolean serverPlugins = null;
	public static String[] groupSuffixPulse = null;
	public static String[] groupSuffixRepeating = null;
	public static Boolean rconEnable = null;
	public static Boolean rconDouble = null;
	public static String rconIP = null;
	public static Integer rconPort = null;
	public static String rconPassword = null;

	public static String[] minecraftCommandsArray = null;
	public static String[] minecraftCommandsExceptionArray = null;
	public static String[] serverOverrideArray = null;
	public static String[] blockArray = null;
	public static String[] selectorArray = null;
	public static String[] targetSelectorArray = null;

	public static void getConfigOptions() {

		GeneralFile configFile = null;

		if (Main.ranInEclpise == true) {
			configFile = new GeneralFile("CCU.ini");
		} else {
			configFile = new GeneralFile(Main.getJarFile + "/" + "CCU.ini");
		}

		ArrayList<String> temp = GeneralFile.removeComment(configFile.getFileArray(), "#", false);
		for (String line : temp) {
			if (line.contains("=")) {
				// returns 1st var
				// System.out.println(line.replace(line.substring(line.indexOf("=")),
				// ""));

				// returns 2nd var
				// System.out.println(line.substring(line.indexOf("=") + 1));

				String tempVar = line.replace(line.substring(line.indexOf("=")), "");
				String tempInput = line.substring(line.indexOf("=") + 1);

				// matches the given text in the ini file
				// with the actual variables
				switch (tempVar) {
				case "mcVersion":
					mcVersion = Integer.parseInt(tempInput);
					break;

				case "regFilePath":
					if (regFilePath == null) {
						regFilePath = new File(tempInput);
					}
					break;
					
				case "globalFilePath":
					globalFilePath = new File(tempInput);
					break;

				case "globalFunctionFilePath":
					globalFunctionFilePath = new File(tempInput);
					break;

				case "importLibraryPath":
					importLibraryPath = new File(tempInput);
					break;

				case "preventServerKick":
					if (tempInput.equalsIgnoreCase("true")) {
						preventServerKick = true;
					} else {
						if (tempInput.equalsIgnoreCase("false")) {
							preventServerKick = false;
						}
					}
					break;

				case "serverPlugins":
					if (tempInput.equalsIgnoreCase("true")) {
						serverPlugins = true;
					} else {
						if (tempInput.equalsIgnoreCase("false")) {
							serverPlugins = false;
						}
					}
					break;

				case "groupSuffixPulse":
					groupSuffixPulse = tempInput.split(",");
					break;

				case "groupSuffixRepeating":
					groupSuffixRepeating = tempInput.split(",");
					break;

				case "rconEnable":
					if (tempInput.equalsIgnoreCase("true")) {
						rconEnable = true;
					} else {
						if (tempInput.equalsIgnoreCase("false")) {
							rconEnable = false;
						}
					}
					break;

				case "rconDouble":
					if (tempInput.equalsIgnoreCase("true")) {
						rconDouble = true;
					} else {
						if (tempInput.equalsIgnoreCase("false")) {
							rconDouble = false;
						}
					}
					break;

				case "rconIP":
					rconIP = tempInput;
					break;

				case "rconPort":
					rconPort = Integer.parseInt(tempInput);
					break;

				case "rconPassword":
					rconPassword = tempInput;
					break;
					
				case "minecraftCommandsArray":
					minecraftCommandsArray = tempInput.split(",");
					break;

				case "minecraftCommandsExceptionArray":
					minecraftCommandsExceptionArray = tempInput.split(",");
					break;

				case "serverOverrideArray":
					serverOverrideArray = tempInput.split(",");
					break;

				case "blockArray":
					blockArray = tempInput.split(",");
					break;

				case "selectorArray":
					selectorArray = tempInput.split(",");
					break;

				case "targetSelectorArray":
					targetSelectorArray = tempInput.split(",");
					break;
				}
			}
		}

		// Checking options
		if (regFilePath == null || regFilePath.toString().length() == 0 && Main.ranInEclpise) {
			System.out.println("ERROR: 'regFilePath' field is empty");
			System.exit(0);
		} else {
			if (regFilePath.isFile() == false) {
				System.out.println("ERROR: " + regFilePath.toString() + " is not a file");
				System.exit(0);
			}
		}

		/*
		if (globalCombinerFilePath == null || globalCombinerFilePath.toString().length() == 0) {
			System.out.println("WARNING: 'globalCombinerFilePath' field is empty");
			System.exit(0);
		} else {
			if (globalCombinerFilePath.isFile() == false) {
				System.out.println("ERROR: " + globalCombinerFilePath.toString() + " is not a file");
				System.exit(0);
			}
		}
		*/
		if (mcVersion == null) {
			System.out.println("WARNING: 'mcVersion' field is empty - defaults to 1.12 (2)");
			mcVersion = 2;
		}

		if (preventServerKick == null) {
			System.out.println("WARNING: 'preventServerKick' field is empty - defaults to 'false'");
			preventServerKick = false;
		}

		if (serverPlugins == null) {
			System.out.println("WARNING: 'serverPlugins' field is empty - defaults to 'false'");
			serverPlugins = false;
		}

		if (groupSuffixPulse == null || groupSuffixPulse[0].equals("")) {
			System.out.println("WARNING: Array 'groupSuffixPulse' field is empty");
		}

		if (groupSuffixRepeating == null || groupSuffixRepeating[0].equals("")) {
			System.out.println("WARNING: Array 'groupSuffixRepeating' field is empty");
		}

		if (rconEnable == null) {
			System.out.println("WARNING: 'rconEnable' field is empty - defaults to 'false'");
			rconEnable = false;
		}

		if (rconEnable == true) {
			if (rconIP == null) {
				System.out.println("ERROR: 'rconIP' field is empty although 'rconEnable' is set to true");
				System.exit(0);
			}
			if (rconPort == null) {
				System.out.println("ERROR: 'rconPort' field is empty although 'rconEnable' is set to true");
				System.exit(0);
			}
			if (rconPassword == null) {
				System.out.println("ERROR: 'rconPassword' field is empty although 'rconEnable' is set to true");
				System.exit(0);
			}

			if (rconDouble == null) {
				System.out.println("WARNING: 'rconDouble' field is empty - defaults to 'false'");
				rconDouble = false;
			}
		}
		
		if (minecraftCommandsArray == null || minecraftCommandsArray[0].equals("")) {
			System.out.println("WARNING: Array 'minecraftCommandsArray' field is empty");
		}
		
		if (ReadConfig.mcVersion >= 2) {
			String[] minecraftCommandsArrayCalc = new String[minecraftCommandsArray.length + 2];
			for (int i = 0; i < minecraftCommandsArray.length; i++) {
				minecraftCommandsArrayCalc[i] = minecraftCommandsArray[i];
			}
			
			// adds if and unless to prevent the execute command from interfering with the function shortcut
			minecraftCommandsArrayCalc[minecraftCommandsArrayCalc.length - 2] = "if";
			minecraftCommandsArrayCalc[minecraftCommandsArrayCalc.length - 1] = "unless";
			minecraftCommandsArray = minecraftCommandsArrayCalc;
		}

		if (minecraftCommandsExceptionArray == null || minecraftCommandsExceptionArray[0].equals("")) {
			System.out.println("WARNING: Array 'minecraftCommandsExceptionArray' field is empty");
		} else {
			ArrayList<String> tempArray = new ArrayList<String>();
			for (String regCmd : minecraftCommandsArray) {
				boolean cannotUseCmd = false;
				for (String cmdExcept : minecraftCommandsExceptionArray) {
					if (cmdExcept.equals(regCmd)) {
						cannotUseCmd = true;
						break;
					}
				}
				
				if (cannotUseCmd == false) {
					tempArray.add(regCmd);
				}
			}
			
			minecraftCommandsArray = new String[tempArray.size()];
			for (int i = 0; i < minecraftCommandsArray.length; i++) {
				minecraftCommandsArray[i] = tempArray.get(i);
			}
		}

		if (serverPlugins == false) {
			serverOverrideArray = null;
		} else {
			if (serverOverrideArray == null || serverOverrideArray[0].equals("")) {
				System.out.println("WARNING: Array 'serverOverrideArray' field is empty");
			}
		}

		if (blockArray == null || blockArray[0].equals("")) {
			System.out.println("ERROR: Array 'blockArray' field is empty");
			System.exit(0);
		}

		if (selectorArray == null || selectorArray[0].equals("")) {
			System.out.println("ERROR: Array 'selectorArray' field is empty");
			System.exit(0);
		}

		if (targetSelectorArray == null || targetSelectorArray[0].equals("")) {
			System.out.println("ERROR: Array 'targetSelectorArray' field is empty");
			System.exit(0);
		}
	}
}
