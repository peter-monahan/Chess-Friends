export async function myFetch(url, options = {}) {
  //set options.method to 'GET' if there is no method
  options.method = options.method || "GET";
  //set options.headers to an empty object if there is no headers
  options.headers = options.headers || {};

  //if the options.method is not 'GET', then 'Content-Type header is set to "application/json".
  if (options.method.toUpperCase() !== "GET") {
    options.headers["Content-Type"] =
      options.headers["Content-Type"] || "application/json";
  }

  //call the default window's fetch with url and the options passed in
  const res = await window.fetch(url, options);

  return res;
}
