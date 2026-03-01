import { createCLI, defineCommand, option } from "@bunli/core";
import { z } from "zod";

function generateOperationId(method: string, path: string): string {
	const segments = path
		.replace(/^\/v\d+\//, "")
		.split("/")
		.map((seg) => {
			const clean = seg.replace(/[{}]/g, "");
			return clean
				.split("_")
				.map((part, i) =>
					i === 0 ? part : part.charAt(0).toUpperCase() + part.slice(1),
				)
				.join("");
		});

	const pathPart = segments
		.map((seg) => seg.charAt(0).toUpperCase() + seg.slice(1))
		.join("");

	return method + pathPart;
}

function addOperationIds(spec: Record<string, unknown>): void {
	const paths = spec.paths as
		| Record<string, Record<string, Record<string, unknown>>>
		| undefined;
	if (!paths) return;

	const httpMethods = new Set([
		"get",
		"post",
		"put",
		"delete",
		"patch",
		"options",
		"head",
	]);

	for (const [path, methods] of Object.entries(paths)) {
		for (const [method, operation] of Object.entries(methods)) {
			if (!httpMethods.has(method)) continue;
			if (operation.operationId) continue;
			operation.operationId = generateOperationId(method, path);
		}
	}
}

function fixMissingParameterSchemas(spec: Record<string, unknown>): void {
	const paths = spec.paths as
		| Record<string, Record<string, Record<string, unknown>>>
		| undefined;
	if (!paths) return;

	const httpMethods = new Set([
		"get",
		"post",
		"put",
		"delete",
		"patch",
		"options",
		"head",
	]);

	for (const methods of Object.values(paths)) {
		for (const [method, operation] of Object.entries(methods)) {
			if (!httpMethods.has(method)) continue;
			const params = operation.parameters as
				| Array<Record<string, unknown>>
				| undefined;
			if (!params) continue;
			for (const param of params) {
				if (!param.schema) {
					param.schema = { type: "string" };
				}
			}
		}
	}
}

function fixEnumSchemaTypes(spec: Record<string, unknown>): void {
	const components = spec.components as Record<string, unknown> | undefined;
	if (!components) return;
	const schemas = components.schemas as
		| Record<string, Record<string, unknown>>
		| undefined;
	if (!schemas) return;

	for (const schema of Object.values(schemas)) {
		if (schema.type === "enum") {
			schema.type = "string";
		}
	}
}

function fixBooleanRequired(obj: unknown): void {
	if (typeof obj !== "object" || obj === null) return;
	if (Array.isArray(obj)) {
		for (const item of obj) fixBooleanRequired(item);
		return;
	}
	const record = obj as Record<string, unknown>;
	const props = record.properties as
		| Record<string, Record<string, unknown>>
		| undefined;
	if (props) {
		const requiredList: string[] = [];
		for (const [name, prop] of Object.entries(props)) {
			if (prop.required === true) {
				requiredList.push(name);
				delete prop.required;
			}
			fixBooleanRequired(prop);
		}
		if (requiredList.length > 0) {
			const existing = Array.isArray(record.required)
				? (record.required as string[])
				: [];
			record.required = [...existing, ...requiredList];
		}
	}
	for (const [key, value] of Object.entries(record)) {
		if (key !== "properties") fixBooleanRequired(value);
	}
}

function fixRefSiblings(obj: unknown): void {
	if (typeof obj !== "object" || obj === null) return;
	if (Array.isArray(obj)) {
		for (const item of obj) fixRefSiblings(item);
		return;
	}
	const record = obj as Record<string, unknown>;
	for (const value of Object.values(record)) {
		fixRefSiblings(value);
	}
	if ("$ref" in record && Object.keys(record).length > 1) {
		const ref = record.$ref;
		delete record.$ref;
		record.allOf = [{ $ref: ref }];
	}
}

function extractSpec(jsSource: string): Record<string, unknown> {
	let captured: Record<string, unknown> | null = null;

	const window: Record<string, unknown> = {
		location: { search: "", origin: "" },
		ui: null,
		onload: null,
	};

	const SwaggerUIBundle = Object.assign(
		(opts: Record<string, unknown>) => {
			captured = (opts.spec ?? opts.swaggerDoc) as Record<string, unknown>;
			return {
				initOAuth() {},
				preauthorizeApiKey: () => true,
				authActions: { authorize() {} },
			};
		},
		{ presets: { apis: null }, plugins: { DownloadUrl: null } },
	);

	const SwaggerUIStandalonePreset = null;
	const setInterval = () => 0;

	// Evaluate the script — it assigns window.onload
	new Function(
		"window",
		"SwaggerUIBundle",
		"SwaggerUIStandalonePreset",
		"setInterval",
		jsSource,
	)(window, SwaggerUIBundle, SwaggerUIStandalonePreset, setInterval);

	// Call the onload handler the script registered
	// biome-ignore lint/complexity/noBannedTypes: DOM hack
	if (typeof window.onload === "function") (window.onload as Function)();

	if (!captured) throw new Error("Failed to capture swaggerDoc from script");
	return captured;
}

const extract = defineCommand({
	name: "extract",
	description: "Extract the OpenAPI spec from Hevy API docs",
	options: {
		url: option(
			z.url().default("https://api.hevyapp.com/docs/swagger-ui-init.js"),
			{
				description: "URL of the swagger-ui-init.js file within hevy docs",
				short: "u",
			},
		),
		output: option(z.string().default("openapi.json"), {
			description: "Output file path",
			short: "o",
		}),
	},
	handler: async ({ flags, spinner }) => {
		const spin = spinner(`Fetching ${flags.url}`);
		spin.start();

		const jsSource = await fetch(flags.url).then((r) => r.text());
		const spec = extractSpec(jsSource);
		addOperationIds(spec);
		fixMissingParameterSchemas(spec);
		fixEnumSchemaTypes(spec);
		fixRefSiblings(spec);
		fixBooleanRequired(spec);

		spin.update(`Writing to ${flags.output}`);
		await Bun.write(flags.output, `${JSON.stringify(spec, null, 2)}\n`);

		spin.succeed(
			`Written to ${flags.output} — ${Object.keys(spec.paths ?? {}).length} paths`,
		);
	},
});

(async () => {
	const cli = await createCLI({
		name: "hevy-extract",
		version: "0.1.0",
		description: "Extract OpenAPI spec from Hevy API docs",
	});

	cli.command(extract);
	await cli.run();
})();
