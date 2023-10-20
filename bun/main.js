import fs from "fs/promises";

const skinApis = [
    "https://crafatar.com/skins/%uuid%",
    "https://minotar.net/skin/%uuid%",
    "https://mineskin.eu/skin/%uuid%",
    "https://api.mineatar.io/skin/%uuid%"
];
let apiCycle = Math.floor(Math.random() * skinApis.length);

for (let e of "0123456789abcdef".split('')) {
	for (let a of "0123456789abcdef".split('')) {
		await fs.mkdir(`./skins/${e + a}/`, {
			recursive: true
		});
	}
}

let stem = readLineStream(Bun.file("q.txt"));

while (true) {
	let { done, value } = await stem.next();
	if (done) break;
	
    let chunkSize = 100;
    let chunks = [];

    for (let i = 0; i < value.length; i += chunkSize) {
        let chunk = value.slice(i, i + chunkSize);
        chunks.push(chunk);
    }

    console.log(value.length, chunks.length);

	for (let chunk of chunks) {
        let start = Date.now();
        let op = chunk.map(async (uuid) => {
            let skin = await fetchSkin(uuid);
            if (skin instanceof ArrayBuffer) {
                await hashAndStore(skin);
            }
        });
        await Promise.all(op);
        console.log("chunk", (Date.now() - start) / 1000);
	}
}

async function hashAndStore(dataBuffer) {
    let hash = new Bun.CryptoHasher("sha256")
        .update(dataBuffer)
        .digest("hex");
    let hashTag = hash.substring(0, 2);
    let filePath = `./skins/${hashTag}/${hash}.png`;

    if (!(await fs.exists(filePath))) {
        await Bun.write(filePath, dataBuffer);
    }
    return hash;
}

async function* readLineStream(file) {
	let overflow = "";
	
	for await (const chunk of file.stream()) {
		let str = overflow + Buffer.from(chunk.buffer).toString();
		let arr = str.split("\r\n");
		let popped = arr.pop();
		overflow = popped;
		yield arr;
	}
}

async function fetchSkin(uuid) {
    apiCycle = (apiCycle + 1) % skinApis.length;
    let url = skinApis[apiCycle].replace(/%uuid%/g, uuid);
    let res;

    try {
        res = await fetch(url, {
            headers: {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
            }
        });
    } catch (err) {
        return null;
    }

    if (res.status !== 200) return null;
    return await res.arrayBuffer();
}

async function fetchUser(user) {
	let url = `https://api.ashcon.app/mojang/v2/user/${user}`;
	let res = await fetch(url);
	let data;

    try {
        data = await res.json();
    } catch (error) {
        return {
            success: false,
            uuid: null,
            skin: null
        };
    }

	if (typeof data?.code == "number") return {
		success: false,
		uuid: null,
		skin: null
	};

	return {
		success: true,
		uuid: data.uuid.replace(/-/g, ''),
		skin: base64ToArrayBuffer(data.textures.skin.data)
	};
}

function base64ToArrayBuffer(base64str) {
	return Uint8Array.from(
		atob(base64str), c => c.charCodeAt(0)
	).buffer;
}
