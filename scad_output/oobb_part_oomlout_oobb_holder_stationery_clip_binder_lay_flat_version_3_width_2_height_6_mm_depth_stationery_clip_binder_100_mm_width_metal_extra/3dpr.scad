$fn = 50;


difference() {
	union() {
		difference() {
			union() {
				translate(v = [0, 0, -3.0000000000]) {
					hull() {
						translate(v = [-17.0000000000, 9.5000000000, 0]) {
							cylinder(h = 6, r = 5);
						}
						translate(v = [17.0000000000, 9.5000000000, 0]) {
							cylinder(h = 6, r = 5);
						}
						translate(v = [-17.0000000000, -9.5000000000, 0]) {
							cylinder(h = 6, r = 5);
						}
						translate(v = [17.0000000000, -9.5000000000, 0]) {
							cylinder(h = 6, r = 5);
						}
					}
				}
			}
			union() {
				translate(v = [-17.2500000000, -37.7500000000, -3.0000000000]) {
					cube(size = [34.5000000000, 30.5000000000, 2.5000000000]);
				}
				translate(v = [-12.2500000000, -7.7500000000, -3.0000000000]) {
					cube(size = [24.5000000000, 8.5000000000, 2.5000000000]);
				}
				#translate(v = [-14.7500000000, -22.7500000000, -3.0000000000]) {
					cube(size = [3.5000000000, 15.5000000000, 6]);
				}
			}
		}
		union() {
			translate(v = [0, -7.5000000000, -3.0000000000]) {
				cylinder(h = 6, r = 7.0000000000);
			}
		}
	}
	union() {
		translate(v = [15, 7.5000000000, 3.0000000000]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						#translate(v = [0, 0, -6.0000000000]) {
							cylinder(h = 6, r = 2.0000000000);
						}
						#translate(v = [0, 0, -3]) {
							cylinder(h = 3, r1 = 2.1250000000, r2 = 3.7500000000);
						}
						#translate(v = [0, 0, -6.0000000000]) {
							cylinder(h = 6, r = 2.1250000000);
						}
						#translate(v = [0, 0, -6.0000000000]) {
							cylinder(h = 6, r = 2.0000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [-15, 7.5000000000, 3.0000000000]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						#translate(v = [0, 0, -6.0000000000]) {
							cylinder(h = 6, r = 2.0000000000);
						}
						#translate(v = [0, 0, -3]) {
							cylinder(h = 3, r1 = 2.1250000000, r2 = 3.7500000000);
						}
						#translate(v = [0, 0, -6.0000000000]) {
							cylinder(h = 6, r = 2.1250000000);
						}
						#translate(v = [0, 0, -6.0000000000]) {
							cylinder(h = 6, r = 2.0000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [0, -7.5000000000, 3.0000000000]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						#translate(v = [0, 0, -6.0000000000]) {
							cylinder(h = 6, r = 2.0000000000);
						}
						#translate(v = [0, 0, -3]) {
							cylinder(h = 3, r1 = 2.1250000000, r2 = 3.7500000000);
						}
						#translate(v = [0, 0, -6.0000000000]) {
							cylinder(h = 6, r = 2.1250000000);
						}
						#translate(v = [0, 0, -6.0000000000]) {
							cylinder(h = 6, r = 2.0000000000);
						}
					}
					union();
				}
			}
		}
	}
}