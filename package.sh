#!/usr/bin/sh

# simple script for cleaning and packaging

case "$1" in
	build)
		# first step, clean up any temporary files we don't want
		echo 'Cleaning environment...'
		find . -name "*~" -type f -delete
		rm -rf install/reorjsd.sh
		rm -rf install/cli.sh
		rm -rf install/node.sh
		rm -rf install/docs.sh
		rm -rf install/install.sh

		#now create our version director
		echo 'Creating package folder'
		mkdir "packages/reorjs-$2"

		#and copy our stuff over
		echo 'Copying version'
		cp -r -L install/* "packages/reorjs-$2"

		#and finally, tarball is
		echo 'Tarballing package'
		cd packages && tar -czf "reorjs-$2.tar.gz" "reorjs-$2"

		echo "Package $2 created!"
		
		echo "Removing copy"

		cd ../ && rm -rf "packages/reorjs-$2"

		echo "Build completed"
	        ;; 
	clean) 
		rm -rf "packages/reorjs-$2"
		rm -rf "packages/reorjs-$2.tar.gz"
	        ;;
	*)
		echo "Unknown command given"
		;;
esac
