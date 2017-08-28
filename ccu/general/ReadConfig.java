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
	public static Boolean toggleEGO = null;
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
		configFile = new GeneralFile(Main.getJarFile + "/" + "CCU.ini");

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
				case "EGO":
					if (tempInput.equalsIgnoreCase("true")) {
						toggleEGO = true;
					} else {
						if (tempInput.equalsIgnoreCase("false")) {
							toggleEGO = false;
						}
					}
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

				case "mcVersion":
					mcVersion = Integer.parseInt(tempInput);
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

		if (toggleEGO == null) {
			toggleEGO = false;
		}

		// Checking options
		if (regFilePath == null || regFilePath.toString().length() == 0) {
			System.out.println("ERROR: 'regFilePath' field is empty");
			System.exit(0);
		} else {
			if (regFilePath.isFile() == false) {
				System.out.println("ERROR: " + regFilePath.toString() + " is not a file");
				System.exit(0);
			} else {
				System.out.println("Compiling file '" + regFilePath.getName() + "'\n");
			}
		}

		if (toggleEGO) { // default EGO settings
			System.out.println("Using default EGO settings (1.10)");
			preventServerKick = true;
			serverPlugins = true;
			rconEnable = false;
			mcVersion = 1;
			// @formatter:off
			String[][] tempStringArray = {
					{"Pulse", "Start", "End"}, // groupSuffixPulse
					{"Clock","Repeat"}, // groupSuffixRepeating
					
					// minecraftCommandsArray
					{"pictionary", "bd", "nobreak", "achievement", "blockdata", "clear", "clone", "debug", "defaultgamemode", "difficulty",
							"effect", "enchant", "entitydata", "execute", "fill", "gamemode", "gamerule", "give", "help", "kill", "me",
							"msg", "particle", "playsound", "publish", "replaceitem", "say", "scoreboard", "seed", "setblock",
							"setworldspawn", "spawnpoint", "spreadplayers", "stats", "stopsound", "summon", "teleport", "tell",
							"tellraw", "testfor", "testforblock", "testforblocks", "time", "title", "toggledownfall", "tp", "trigger",
							"w", "weather", "worldborder", "xp"},
					{"execute"}, // minecraftCommandsExceptionArray
					{"kill","clear","xp","tp","teleport","gamemode"}, // serverOverrideArray
					
					// blockArray
					{"acacia_door", "acacia_fence", "acacia_fence_gate", "acacia_stairs", "activator_rail", "air", "anvil", "barrier",
							"beacon", "bed", "bedrock", "beetroots", "birch_door", "birch_fence", "birch_fence_gate", "birch_stairs",
							"bone_block", "bookshelf", "brewing_stand", "brick_block", "brick_stairs", "brown_mushroom",
							"brown_mushroom_block", "cactus", "cake", "carpet", "carrots", "cauldron", "chain_command_block", "chest",
							"chorus_flower", "chorus_plant", "clay", "coal_block", "coal_ore", "cobblestone", "cobblestone_wall",
							"cocoa", "command_block", "crafting_table", "dark_oak_door", "dark_oak_fence", "dark_oak_fence_gate",
							"dark_oak_stairs", "daylight_detector", "daylight_detector_inverted", "deadbush", "detector_rail",
							"diamond_block", "diamond_ore", "dirt", "dispenser", "double_plant", "double_stone_slab",
							"double_stone_slab2", "double_wooden_slab", "dragon_egg", "dropper", "emerald_block", "emerald_ore",
							"enchanting_table", "end_bricks", "end_gateway", "end_portal", "end_portal_frame", "end_rod", "end_stone",
							"ender_chest", "farmland", "fence", "fence_gate", "fire", "flower_pot", "flowing_lava", "flowing_water",
							"frosted_ice", "furnace", "glass", "glass_pane", "glowstone", "gold_block", "gold_ore", "golden_rail",
							"grass", "grass_path", "gravel", "hardened_clay", "hay_block", "heavy_weighted_pressure_plate", "hopper",
							"ice", "iron_bars", "iron_block", "iron_door", "iron_ore", "iron_trapdoor", "jukebox", "jungle_door",
							"jungle_fence", "jungle_fence_gate", "jungle_stairs", "ladder", "lapis_block", "lapis_ore", "lava",
							"leaves", "leaves2", "lever", "light_weighted_pressure_plate", "lit_furnace", "lit_pumpkin",
							"lit_redstone_lamp", "lit_redstone_ore", "log", "log2", "magma", "melon_block", "melon_stem",
							"mob_spawner", "monster_egg", "mossy_cobblestone", "mycelium", "nether_brick", "nether_brick_fence",
							"nether_brick_stairs", "nether_wart", "nether_wart_block", "netherrack", "noteblock", "oak_stairs",
							"obsidian", "packed_ice", "piston", "piston_extension", "piston_head", "planks", "portal", "potatoes",
							"powered_comparator", "powered_repeater", "prismarine", "pumpkin", "pumpkin_stem", "purpur_block",
							"purpur_double_slab", "purpur_pillar", "purpur_slab", "purpur_stairs", "quartz_block", "quartz_ore",
							"quartz_stairs", "rail", "red_flower", "red_mushroom", "red_mushroom_block", "red_nether_brick",
							"red_sandstone", "red_sandstone_stairs", "redstone_block", "redstone_lamp", "redstone_ore",
							"redstone_torch", "redstone_wire", "reeds", "repeating_command_block", "sand", "sandstone",
							"sandstone_stairs", "sapling", "sea_lantern", "skull", "slime", "snow", "snow_layer", "soul_sand",
							"sponge", "spruce_door", "spruce_fence", "spruce_fence_gate", "spruce_stairs", "stained_glass",
							"stained_glass_pane", "stained_hardened_clay", "standing_banner", "standing_sign", "sticky_piston",
							"stone", "stone_brick_stairs", "stone_button", "stone_pressure_plate", "stone_slab", "stone_slab2",
							"stone_stairs", "stonebrick", "structure_block", "structure_void", "tallgrass", "tnt", "torch", "trapdoor",
							"trapped_chest", "tripwire", "tripwire_hook", "unlit_redstone_torch", "unpowered_comparator",
							"unpowered_repeater", "vine", "wall_banner", "wall_sign", "water", "waterlily", "web", "wheat",
							"wooden_button", "wooden_door", "wooden_pressure_plate", "wooden_slab", "wool", "yellow_flower"},
					{"@a","@e","@r","@p"}, // selectorArray
					
					// targetSelectorArray
					{"x","y","z","r","rm","dx","dy","dz","tag","team","type","c","l","lm","m","name","rx","rxm","ry","rym"}
			};
			// @formatter:on

			groupSuffixPulse = tempStringArray[0];
			groupSuffixRepeating = tempStringArray[1];
			minecraftCommandsArray = tempStringArray[2];
			minecraftCommandsExceptionArray = tempStringArray[3];
			serverOverrideArray = tempStringArray[4];
			blockArray = tempStringArray[5];
			selectorArray = tempStringArray[6];
			targetSelectorArray = tempStringArray[7];
			
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

		if (mcVersion == null) {
			System.out.println("WARNING: 'mcVersion' field is empty - defaults to 1.12 (2)");
			mcVersion = 2;
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
