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
import ccu.mcfunction.FunctionNick;
import ccu.mcfunction.WriteFile;
import ccu.rcon.MinecraftRcon;

public class Main {
	/* TODO
	 * -Special comments using #
	 * 
	 * General statements
	 * -FILE
	 */

	// .replaceAll("^\\s+", "") = space to the left
	// .replaceAll("\\s+$", "") = space to the right

	public static File getJarFile = null;

	public static void main(String[] args) {
		long startTime = System.nanoTime();

		// checks version
		String currentVersion = "1.1.1";
		System.out.println("Current version: " + currentVersion);

		try {
			URL url;
			url = new URL("https://raw.githubusercontent.com/Aquafina-water-bottle/Command-Compiler-Unlimited/master/version.txt");

			URLConnection con = url.openConnection();
			InputStream is = con.getInputStream();
			BufferedReader br = new BufferedReader(new InputStreamReader(is));
			String getVersion = br.readLine();

			if (StringUtils.countChars(currentVersion, ".") == 1) {
				currentVersion += ".0";
			}

			if (StringUtils.countChars(getVersion, ".") == 1) {
				getVersion += ".0";
			}

			String[] currentVersionCalc = currentVersion.split("\\.");
			String[] getVersionCalc = getVersion.split("\\.");

			boolean outdatedVersion = true;
			if (Integer.parseInt(currentVersionCalc[0]) >= Integer.parseInt(getVersionCalc[0])
					|| Integer.parseInt(currentVersionCalc[1]) >= Integer.parseInt(getVersionCalc[1])
					|| Integer.parseInt(currentVersionCalc[2]) >= Integer.parseInt(getVersionCalc[2])) {
				outdatedVersion = false;
			}

			if (outdatedVersion) {
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
		if (args.length >= 1) {
			ReadConfig.regFilePath = new File(args[0]);
		}

		getJarFile = new File(ClassLoader.getSystemClassLoader().getResource(".").getPath().replace("%20", " "));

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

		// Gets the function nicknames and uses the filePathFuncOption option
		FunctionNick.setFunctionNicks();

		// Writes the mcfunction files since it's literally the easiest thing to do lmao
		WriteFile.writeMCFunction();

		// Writes the _commands, _parsed, and _combiner files
		Setblock.getCommands();

		// RCON
		MinecraftRcon.useRcon();

		long endTime = System.nanoTime();
		System.out.println("\nSuccessfully compiled the file '" + ReadConfig.regFilePath.getName() + "' in "
				+ ((endTime - startTime) / 1e9) + " seconds");
	}
}
