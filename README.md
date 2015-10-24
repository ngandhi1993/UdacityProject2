Following is a step by step process on how to perform the tests:-

1. Go to the rootdirectory of this Github repo and perform `vagrant up` in the vagrant directory to get the virtual machine to set up.
2. `vagrant ssh` to ssh into the virtual machine
3. Go to the `/vagrant` directory which will have all the shared files, same as that in your project directory on the laptop.
4. Run the psql commandline by simply running `psql`
5. Run `\i tournament.sql` to get the database created.
6. Exit out of psql
7. You can now run the test by running `python tournament_test.py` in the tournament directory.
8. Your tests should pass.
