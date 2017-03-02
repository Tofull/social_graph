## Exemples
### Create the graph
```
create (facebook:Social {nom:"facebook"})
create (twitter:Social {nom:"twitter"})
create (linkedin:Social {nom:"linkedin"})

create (roger:Personne {nom:"roger"})
create (roger)-[:INSCRIT]->(facebook)

create (mimi:Personne {nom:"mimi"})
create (mimi)-[:INSCRIT]->(facebook)

create (roger)-[:COUPLE]->(mimi)
```

### Request the graph
```
MATCH (roger:Personne { nom:"roger" })-[:COUPLE]-(mimi:Personne {nom:"mimi"})
RETURN roger, mimi
```

## Notes :
### Bi-Directional Relationships
Certain relationships are implicitly bi-directional, such as the KNOWS relationship we created in the example where there are two relationships between Jack and Jill. In these cases it can provide read query flexibility, but adds additional write load and requires more maintenance to have both. Much of this strategy will come down to your use case, but when possible I’ve found it easier to only create one relationship and always MATCH without direction specified to detect its existence for relationships that are implicitly bi-directional where there is no variation between INCOMING and OUTGOING relationships.
