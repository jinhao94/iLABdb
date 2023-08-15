args=commandArgs(T)
#print(length(args))
if(length(args)!=4){
    return(message("Useage: Rscript iLABdb.growth.rate.calculation.R gene.ffn CDS.names gene.info"))    
}

print("------Running--------")


suppressPackageStartupMessages(library("gRodon"))
suppressPackageStartupMessages(library("Biostrings"))
suppressPackageStartupMessages(library("dplyr"))
suppressPackageStartupMessages(library("plyr"))

#library(gRodon)
#library(Biostrings)
#library(dplyr)
#library(plyr)

gene.file=args[1]
CDS.file=args[2]
gene.info.file=args[3]
Growth.rate.res=args[4]

## growth rate
genes <- readDNAStringSet(gene.file)
gene_info <-  readLines(gene.info.file)
highly_expressed <- grepl("S ribosomal protein", gene_info, ignore.case = T)
CDS_IDs <- readLines(CDS.file)
gene_IDs <- gsub(" .*","",names(genes)) #Just look at first part of name before the space
genes <- genes[gene_IDs %in% CDS_IDs]
res = predictGrowth(genes, highly_expressed, mode="partial") %>% ldply()
colnames(res) = c("Item", "Value")
write.table(res, file=Growth.rate.res, quote=F, row.names=F)


print("------Done--------")
