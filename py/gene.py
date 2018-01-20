from Bio import Entrez

def search(query):
	Entrez.email = 'test@gmail.com'
	handle = Entrez.esearch(db='gene',
				sort='relevance',
				retmax='20',
				retmode='xml',
				term=query)

	results = Entrez.read(handle)
	return results

def fetch_detail_single(id):
	Entrez.email = 'test@gmail.com'
	handle = Entrez.efetch(db='gene',
				retmode='xml',
				id=id)
	results = Entrez.read(handle)
	return results

def fetch_details(id_list):
	ids = ','.join(id_list)
	Entrez.email = 'test@gmail.com'
	handle = Entrez.efetch(db='gene',
				retmode='xml',
				id=ids)
	results = Entrez.read(handle)
	return results

if __name__ == '__main__':
	# user_input = input()

	query = 'hepatocellular carcinoma[All Fields] AND (resistance[All Fields] OR prognosis[All Fields] OR metastasis[All Fields] OR recurrence[All Fields] OR survival[All Fields] OR carcinogenesis[All Fields] OR sorafenib[All Fields] OR bevacizumab[All Fields]) AND alive[prop]'
	results = search(query)
	print(type(results))
	print(results)
	id_list = results['IdList']
	print(id_list)
	papers = fetch_details(id_list)
	entrez_gene = 'Entrezgene_gene'
	gene_ref = 'Gene-ref'
	gene_locus = 'Gene-ref_locus'

	print(type(papers))
	for i in range(len(papers)):
		print(papers[i][entrez_gene][gene_ref][gene_locus])

#	for key in papers:
#		print('TYPE:', type(key), key, ': \n')
#		for key2 in papers[key]:
#			print(key2, ":::", papers[key])
#	for i, paper in enumerate(papers):
#		print("%d) %s"
#			% (i+1,
#	paper['MedlineCitation']['Article']['ArticleTitle']))


# Pretty print the first paper in full to observe its structure
#import json
#print(json.dumps(papers[0], indent=2, separators=(',', ':')))
