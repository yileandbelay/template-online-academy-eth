// Stand-in for nginx gzip in front of the Flask baseline: node gzip-proxy.js <listen> <target>
const http = require('http'); const zlib = require('zlib');
const [listen, target] = [Number(process.argv[2]), Number(process.argv[3])];
http.createServer((req, res) => {
  const p = http.request({ host: '127.0.0.1', port: target, path: req.url, method: req.method, headers: { ...req.headers, 'accept-encoding': 'identity' } }, (r) => {
    const type = r.headers['content-type'] || ''; const headers = { ...r.headers };
    if (/text|css|javascript|json|svg/.test(type) && /gzip/.test(req.headers['accept-encoding'] || '')) {
      delete headers['content-length']; headers['content-encoding'] = 'gzip';
      res.writeHead(r.statusCode, headers); r.pipe(zlib.createGzip({ level: 6 })).pipe(res);
    } else { res.writeHead(r.statusCode, headers); r.pipe(res); }
  });
  req.pipe(p);
}).listen(listen, '127.0.0.1');
