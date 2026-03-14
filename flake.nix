{
  description = "YoutubeRSS – YouTube channels/playlists as podcast RSS feeds";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      forAllSystems = nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3;
          pythonPkgs = python.pkgs;
        in
        {
          default = pkgs.mkShell {
            packages = [
              (python.withPackages (ps: [
                ps.flask
                ps.requests
                ps.yt-dlp
                ps.gunicorn
                # dev tools
                ps.pytest
                ps.black
                ps.ipython
              ]))
            ];
          };
        }
      );

      packages = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3;
        in
        {
          default = pkgs.writeShellScriptBin "youtuberss" ''
            export PYTHONPATH="${self}:''${PYTHONPATH:-}"
            exec ${python.withPackages (ps: [
              ps.flask
              ps.requests
              ps.yt-dlp
              ps.gunicorn
            ])}/bin/gunicorn \
              --bind 0.0.0.0:8080 \
              --workers 2 \
              --timeout 120 \
              wsgi:app "$@"
          '';
        }
      );

      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/youtuberss";
        };
      });
    };
}
