for i in {1..11}
  do
   echo "-------------------------Executing Iteration : $i"
   ./gtaf_contacts_suite.sh | tee out_$i.log
   sleep 5 
  done 
