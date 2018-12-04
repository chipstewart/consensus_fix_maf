task consensus_fix_maf_task_1 {
    
    File input_consensus_maf
    File input_oncotated_maf
    String id

    Float? ram_gb
    Int? local_disk_gb
    Int? num_preemptions

    #**Define additional inputs here**

    command {
        set -euo pipefail

  echo "${NALT_thresh}"

        echo "${input_consensus_maf}"
        echo "${input_oncotated_maf}"

        ls -lath

        python /opt/src/fix_consensus_maf.py -C ${input_consensus_maf} -O ${input_oncotated_maf} -i ${id} 
    }

    output {
        File consensus_fix_maf="${id}.fix.maf"
    }

    runtime {
        docker : "chipstewart/consensus_fix_maf_task_1:1"
        memory: "${if defined(ram_gb) then ram_gb else '2'}GB"
        disks : "local-disk ${if defined(local_disk_gb) then local_disk_gb else '10'} HDD"
        preemptible : "${if defined(num_preemptions) then num_preemptions else '3'}"
    }

    meta {
        author : "Chip Stewart"
        email : "stewart@broadinstitute.org"
    }
}

workflow consensus_fix_maf {

    call consensus_fix_maf_task_1 

}
