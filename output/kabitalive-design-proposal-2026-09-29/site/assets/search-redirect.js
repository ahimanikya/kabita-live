// Keep the journal's relative base path and saved search/filter parameters.
location.replace(new URL('poems.html' + location.search + location.hash, location.href).href);
