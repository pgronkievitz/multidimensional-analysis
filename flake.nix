{
  description = "Python project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";

    pypi-deps-db.url = "github:DavHau/mach-nix/3.4.0";
    mach-nix = {
      url = "github:DavHau/mach-nix/3.4.0";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
      inputs.pypi-deps-db.follows = "pypi-deps-db";
    };
  };

  outputs = { self, nixpkgs, flake-utils, mach-nix, ... }@attr:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = "python39";
        mach = import mach-nix { inherit pkgs python; };

        myPython = (mach.mkPython {
          requirements = builtins.readFile ./requirements.txt;
          providers._default = "wheel,sdist,nixpkgs,conda";
        });
      in { devShell = pkgs.mkShell { nativeBuildInputs = [ myPython ]; }; });
}
