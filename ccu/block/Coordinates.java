package ccu.block;

import ccu.command.Var_Options;
import ccu.general.GeneralFile;
import ccu.general.NumberUtils;

public class Coordinates {
	// Okay technically I copied/pasted this class from CBP
	// however, I edited it a lot to the point where I'm about 99% sure it's not even close to
	// what it previously was so I guess this is fine idk
	private int x;
	private int y;
	private int z;
	private String relativeX = "";
	private String relativeY = "";
	private String relativeZ = "";

	// Constructor if coordinates aren't specified

	public Coordinates() {
		this(0, 0, 0);
	}

	// Constructor if coordinates are specified
	public Coordinates(int x, int y, int z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}

	// Constructor specifically for relative coordinates
	public Coordinates(int x, int y, int z, String relativeX, String relativeY, String relativeZ) {
		this.x = x;
		this.y = y;
		this.z = z;
		this.relativeX = relativeX;
		this.relativeY = relativeY;
		this.relativeZ = relativeZ;
	}

	// Constructor for string
	public Coordinates(String getCoords) {
		String[] calcArray = null;
		calcArray = getCoords.split(" ");

		if (calcArray.length == 3) {
			for (int i = 0; i < calcArray.length; i++) {
				if (calcArray[i].contains("~")) {
					
					if (i == 0) {
						this.relativeX = "~";
					}
					if (i == 1) {
						this.relativeY = "~";
					}
					if (i == 2) {
						this.relativeZ = "~";
					}
					
					calcArray[i] = calcArray[i].replace("~", "");
				}
				if (NumberUtils.isNum(calcArray[i])) {
					if (i == 0) {
						this.x = Integer.parseInt(calcArray[i]);
					}
					if (i == 1) {
						this.y = Integer.parseInt(calcArray[i]);
					}
					if (i == 2) {
						this.z = Integer.parseInt(calcArray[i]);
					}
					
				} else {
					System.out.println("ERROR: Coordinates '" + getCoords + "' have to be a set of 3 numbers");
					System.exit(0);
				}
			}

		} else {
			System.out.println("ERROR: Coordinates '" + getCoords + "' have to be a set of 3 numbers");
			System.exit(0);
		}
	}

	// Seeing if coordinates should be relative
	/*
	public void RelativeCoords(boolean x, boolean y, boolean z) {
		this.relativeX = x;
		this.relativeY = y;
		this.relativeZ = z;
	}*/

	/*
	// Constructor for array
	public Coordinates(int[] coor) {
		if ((coor == null) || (coor.length != 3)) {
			coor = new int[3];
		} else {
			System.out.println("wtf is this");
			System.out.println(coor);
		}
		this.x = coor[0];
		this.y = coor[1];
		this.z = coor[2];
		// System.out.println(this.x + " " + this.y + " " + this.z);
	}*/

	// Set coordinates
	/*
	public void setCoordinates(int x, int y, int z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}*/

	// Set coordinates using a string
	public void setCoordinates(String coords) {
		final String[] tempCoordsArray = coords.split(" ");
		if (tempCoordsArray.length == 3) {
			if (tempCoordsArray[0].substring(0, 1).equals("~")) {
				relativeX = "~";
				tempCoordsArray[0] = tempCoordsArray[0].substring(1);
			}
			if (tempCoordsArray[1].substring(0, 1).equals("~")) {
				relativeY = "~";
				tempCoordsArray[1] = tempCoordsArray[1].substring(1);
			}
			if (tempCoordsArray[2].substring(0, 1).equals("~")) {
				relativeZ = "~";
				tempCoordsArray[2] = tempCoordsArray[2].substring(1);
			}
			try {
				this.x = Integer.parseInt(tempCoordsArray[0]);
				this.y = Integer.parseInt(tempCoordsArray[1]);
				this.z = Integer.parseInt(tempCoordsArray[2]);
			} catch (NumberFormatException e) {
				System.out.println("ERROR: coordsOption must be in integers");
				System.exit(0);
			} catch (Exception e) {
				GeneralFile.dispError(e);
				System.exit(0);
			}
		} else {
			System.out.println("ERROR: coordsOption contains an incorrect number of coordinate values (must be 3)");
			System.exit(0);
		}
	}

	// Add coordinates
	public Coordinates addCoordinates(Coordinates coor) {
		this.x += coor.x;
		this.y += coor.y;
		this.z += coor.z;

		if (coor.relativeX.equals("~")) {
			this.relativeX = "~";
		}
		if (coor.relativeY.equals("~")) {
			this.relativeY = "~";
		}
		if (coor.relativeZ.equals("~")) {
			this.relativeZ = "~";
		}

		return this;
	}

	public Coordinates addCoordinates(int x, int y, int z) {
		this.x += x;
		this.y += y;
		this.z += z;
		return this;
	}

	// Add offset
	public Coordinates addOffset(int[] offset) {
		if ((offset == null) || (offset.length != 3)) {
			offset = new int[3];
		}
		this.x += offset[0];
		this.y += offset[1];
		this.z += offset[2];
		return this;
	}

	public Coordinates switchDirection() {
		int tempZ = this.z;
		int tempX = this.x;
		if (GroupStructure.styleOptionXZ.equals("+Z")) {
			this.z = tempX + 0;
			this.x = tempZ + 0;
			return this;
		} else {
			if (GroupStructure.styleOptionXZ.equals("-Z")) {
				this.z = 16 - tempX;
				this.x = 16 - tempZ;
				return this;
			} else {
				if (GroupStructure.styleOptionXZ.equals("-X")) {
					tempX = 16 - this.z;
					tempZ = 16 - this.x;
					this.z = tempX + 0;
					this.x = tempZ + 0;
					return this;
				} else {
					if (GroupStructure.styleOptionXZ.equals("+X") == false) {
						System.out.println("ERROR: Option styleOption '" + Var_Options.styleOption + "' is invalid");
						System.exit(0);
					}
				}
			}
		}
		return this;
	}

	public boolean isRelative() {
		if (this.relativeX.equals("~") || this.relativeY.equals("~") || this.relativeZ.equals("~")) {
			return true;
		} else {
			return false;
		}
	}

	// if the coordinate is relative, it takes the coordinates - given coordinates
	public Coordinates checkRelative(Coordinates getCoords) {
		int tempX = this.x + 0;
		int tempY = this.y + 0;
		int tempZ = this.z + 0;

		if (this.relativeX.equals("~")) {
			tempX = this.x - getCoords.x;
		}

		if (this.relativeY.equals("~")) {
			tempY = this.y - getCoords.y;
		}

		if (this.relativeZ.equals("~")) {
			tempZ = this.z - getCoords.z;
		}

		return new Coordinates(tempX, tempY, tempZ, this.relativeX, this.relativeY, this.relativeZ);
	}

	public int getX() {
		return this.x;
	}

	public int getY() {
		return this.y;
	}

	public int getZ() {
		return this.z;
	}

	public int[] getArray() {
		return new int[] {this.x, this.y, this.z};
	}

	// get string
	public String getString() {
		return this.relativeX + this.x + " " + this.relativeY + this.y + " " + this.relativeZ + this.z;
	}
}
