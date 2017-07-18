package ccu.general;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import ccu.block.Box;
import ccu.block.GroupStructure;
import ccu.block.Setblock;
import ccu.command.ReadCCUFile;
import ccu.command.Var_Options;
import ccu.mcfunction.WriteFile;
import ccu.rcon.MinecraftRcon;

public class Main {
	/* TODO
	 * For the program
	 * -Combiners - DONE
	 * -Scoreboard shortcuts - DONE
	 * -Execute shortcuts - DONE
	 * -Selector shortcuts - DONE
	 * -Definitions working with COORDS and TELE - DONE
	 * -Definitions within definitions - DONE
	 * -Usage of BRANCH via MFUNC - DONE
	 * -MFUNC nicknames - DONE
	 * -Server override using 'minecraft:' when detecing commands exist - DONE
	 * -Putting MFUNC into the parsed file - DONE
	 * -Skipping lines using ';' - DONE
	 * 
	 * -FUNC - DONE (now with proper future params)
	 * -IMPORT - DONE (without importing .dat files)
	 * -UNASSIGN - DONE (since arrays, team lists and objective lists aren't a thing yet)
	 * -LOOP - DONE (completely woot)
	 * -IF - DONE (completely WOOOT)
	 * -SIN COS TAN CALC - DONE WOOOOOOOOOT
	 * -ARRAY - DONE WOOOOOOOOOOOOOOOOOOOOOT
	 * -SPLIT - DONE AS FUCK
	 * 
	 * -Repeated definitions - Already works apparently
	 * -Check whether commands exist - WILL NOT DO
	 * 
	 * -Better RCON usage - do when multiparse works
	 * -Combiner options using .mcfunction - do when multiparse works
	 * -Save coords option
	 * -Multiparse
	 * -Fix Recurring imports
	 * -Multithreading when checking for the version
	 * -Making DEF only use COORDS (and remove tele), and detect whether it's 3, 4, 5 or 6 numbers
	 * 
	 * General statements
	 * -INITIALIZE
	 * -FILE
	 * 

	 * -PARSE
	 * -Escaping using '`'
	 * -Escaping using '/' at the beginning of a line
	 * 
	 */

	// .replaceAll("^\\s+", "") = space to the left
	// .replaceAll("\\s+$", "") = space to the right

	public static File getJarFile = null;

	public static void main(String[] args) {
		long startTime = System.nanoTime();
		
		// checks version
		String currentVersion = "Build 6";
		System.out.println("Current: " + currentVersion);
		
		try {
			URL url;
			url = new URL("https://raw.githubusercontent.com/Aquafina-water-bottle/Command-Compiler-Unlimited/master/CCUVersion.txt");

			URLConnection con = url.openConnection();
			InputStream is = con.getInputStream();
			BufferedReader br = new BufferedReader(new InputStreamReader(is));
			String getVersion = br.readLine();

			if (currentVersion.equals(getVersion) == false) {
				System.out.println("An update is avaliable for CCU (" + getVersion
						+ ") at 'https://github.com/Aquafina-water-bottle/Command-Compiler-Unlimited/releases'");
				TimeUnit.SECONDS.sleep(1);
			}
		} catch (IOException e) {
			System.out.println("WARNING: URL to check versions cannot be found");
		} catch (InterruptedException e) {
			GeneralFile.dispError(e);
		}
		
		System.out.println("");

		// for CCU_NPP.bat
		if (args.length == 1) {
			getJarFile = new File(args[0]);
		}
		if (args.length == 2) {
			ReadConfig.regFilePath = new File(args[0]);
			getJarFile = new File(args[1]);
		}

		// String asdf = "this is a CALC(1 + SIN((1 - 2.0)) * (13 - 3)) asdf)";
		// MathParser.parseSecondaryStatements(asdf, asdf);

		// Reads the .ini file and gets the options
		ReadConfig.getConfigOptions();

		if (ReadConfig.regFilePath.toString().endsWith(".ccu") == false) {
			System.out.println("ERROR: File does not end with '.ccu'");
			System.exit(0);
		}

		// Reads the file stated in the .ini file
		ReadCCUFile ccuFile = new ReadCCUFile(ReadConfig.regFilePath);

		// Parses all CCU statements including defines
		ArrayList<String> getCommandsArray = ccuFile.checkCommands();

		// Checks if any options are left blank, and sets them to a default value if they are
		Var_Options.checkOptions();

		// for (String asdf : getCommandsArray) {
		//	System.out.println(asdf);
		// }

		// This pretty much only runs if something isn't encapsulated with MFUNC or GROUP
		if (getCommandsArray != null && getCommandsArray.isEmpty() == false) {

			System.out.println("\tERROR: Unnused commands in lines:");
			for (String line : getCommandsArray) {
				System.out.println("'" + line + "'");
			}
			System.exit(0);
		}

		// Get the structures for each command block group
		GroupStructure.getGroupStructures();

		// Gets the full arrangement of structures
		Box.getBox();

		// Finalizes all commands with "setblock groupName" and "fill groupName"
		// Also writes the name_dat.ccu file
		Box.finalizeCoords();

		// Writes the mcfunction files since it's literally the easiest thing to do lmao
		WriteFile.writeMCFunction();

		// Writes the _commands, _parsed, and _combiner files
		Setblock.getCommands();

		// Writes the global Combiner file under globalCombinerFilePath

		// RCON
		MinecraftRcon.useRcon();

		long endTime = System.nanoTime();
		System.out.println("\nSuccessfully compiled the file '" + ReadConfig.regFilePath.getName() + "' in "
				+ ((endTime - startTime) / 1e9) + " seconds");
	}
}
