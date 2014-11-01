#!/usr/bin/sh

# simple script for cleaning and packaging

case "$1" in
	build)
		# first step, clean up any temporary files we don't want
		echo 'Cleaning environment...'
		find . -name "*~" -type f -delete

		#the all package
		rm -rf install/all/reorjsd.sh
		rm -rf install/all/cli.sh
		rm -rf install/all/node.sh
		rm -rf install/all/docs.sh
		rm -rf install/all/install.sh

		#the reorjsd package
		rm -rf install/reorjsd/reorjsd.sh
		rm -rf install/reorjsd/cli.sh
		rm -rf install/reorjsd/node.sh
		rm -rf install/reorjsd/docs.sh
		rm -rf install/reorjsd/install.sh
		
		#the cli package
		rm -rf install/reorjs-cli/reorjsd.sh
		rm -rf install/reorjs-cli/cli.sh
		rm -rf install/reorjs-cli/node.sh
		rm -rf install/reorjs-cli/docs.sh
		rm -rf install/reorjs-cli/install.sh
		
		#the node package
		rm -rf install/reorjs-node/reorjsd.sh
		rm -rf install/reorjs-node/cli.sh
		rm -rf install/reorjs-node/node.sh
		rm -rf install/reorjs-node/docs.sh
		rm -rf install/reorjs-node/install.sh
	
		##
		# create our all package
		##
	
		#now create our version directory
		echo 'Creating package folder'
		mkdir "packages/reorjs-$2"

		#and copy our stuff over
		echo 'Copying version'
		cp -r -L install/all/* "packages/reorjs-$2"

		#and finally, tarball is
		echo 'Tarballing package'
		cd packages && tar -czf "reorjs-$2.tar.gz" "reorjs-$2"

		echo "Package $2 created!"
		
		echo "Removing copy"

		cd ../ && rm -rf "packages/reorjs-$2"

		##
		# create our reorjs package
		##
	
		#now create our version directory
		echo 'Creating package folder'
		mkdir "packages/reorjsd-$2"

		#and copy our stuff over
		echo 'Copying version'
		cp -r -L install/reorjsd/* "packages/reorjsd-$2"

		#and finally, tarball is
		echo 'Tarballing package'
		cd packages && tar -czf "reorjsd-$2.tar.gz" "reorjsd-$2"

		echo "Package reorjsd-$2 created!"
		
		echo "Removing copy"

		cd ../ && rm -rf "packages/reorjsd-$2"

		##
		# create our reorjs-cli package
		##
	
		#now create our version directory
		echo 'Creating package folder'
		mkdir "packages/reorjs-cli-$2"

		#and copy our stuff over
		echo 'Copying version'
		cp -r -L install/reorjs-cli/* "packages/reorjs-cli-$2"

		#and finally, tarball is
		echo 'Tarballing package'
		cd packages && tar -czf "reorjs-cli-$2.tar.gz" "reorjs-cli-$2"

		echo "Package reorjs-cli-$2 created!"
		
		echo "Removing copy"

		cd ../ && rm -rf "packages/reorjs-cli-$2"

		##
		# create our reorjs-node package
		##
	
		#now create our version directory
		echo 'Creating package folder'
		mkdir "packages/reorjs-node-$2"

		#and copy our stuff over
		echo 'Copying version'
		cp -r -L install/reorjs-node/* "packages/reorjs-node-$2"

		#and finally, tarball is
		echo 'Tarballing package'
		cd packages && tar -czf "reorjs-node-$2.tar.gz" "reorjs-node-$2"

		echo "Package reorjs-node-$2 created!"
		
		echo "Removing copy"

		cd ../ && rm -rf "packages/reorjs-node-$2"

		echo "Build completed"
	        ;; 
	clean) 
		rm -rf "packages/reorjs-$2"
		rm -rf "packages/reorjs-$2.tar.gz"
	        ;;
	libs)
		echo "Starting construction of $2 libs"
		echo "Will create version $3"
		
		echo "Moving current version to old dir"
		mv "packages/libs/reorjs-$2"* "packages/old/libs"
		
		echo "Creating temporary directory"
		mkdir "packages/reorjs-$2-$3"
		
		echo "Copying files"
		cp -r -L "lib/$2/"* "packages/reorjs-$2-$3/"
		
		echo "Tarballing package"
		cd packages && tar -czf "reorjs-$2-$3.tar.gz" "reorjs-$2-$3"
		
		echo "Package reorjs-$2-$3 created!"
		
		echo "Removing copy"
		
		cd ../ && rm -rf "packages/reorjs-$2-$3"
		
		echo "Moving to libs"
		
		mv "packages/reorjs-$2-$3.tar.gz" "packages/libs/"
		
		echo "Build completed"		
		;;
	*)
		echo "Unknown command given"
		;;
esac
