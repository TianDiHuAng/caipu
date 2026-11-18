// 零依赖 JSON Schema (draft-07 子集) 校验器
// 支持: type / required / properties / additionalProperties / items / minItems / maxItems
//       minLength / maxLength / minimum / maximum / exclusiveMinimum / exclusiveMaximum
//       enum / const / pattern / oneOf / anyOf / allOf / $ref(本地 #/definitions/*)

export class SchemaError extends Error {}

function typeOf(v) {
  if (v === null) return 'null';
  if (Array.isArray(v)) return 'array';
  if (Number.isInteger(v)) return 'integer';
  return typeof v;
}

function typeMatches(value, t) {
  const actual = typeOf(value);
  if (t === 'number') return actual === 'number' || actual === 'integer';
  if (t === 'integer') return actual === 'integer';
  return actual === t;
}

function resolveRef(root, ref) {
  if (!ref.startsWith('#/')) throw new SchemaError('不支持的 $ref: ' + ref);
  const parts = ref.slice(2).split('/');
  let node = root;
  for (const p of parts) {
    node = node?.[p];
    if (node === undefined) throw new SchemaError('无法解析 $ref: ' + ref);
  }
  return node;
}

/**
 * @returns {string[]} 错误列表，空数组表示通过
 */
export function validate(schema, value, root = schema, path = '$') {
  if (schema === true || schema === undefined) return [];
  if (schema === false) return [`${path}: 该字段不允许出现`];
  if (schema.$ref) return validate(resolveRef(root, schema.$ref), value, root, path);

  const errors = [];

  if (schema.type !== undefined) {
    const types = Array.isArray(schema.type) ? schema.type : [schema.type];
    if (!types.some((t) => typeMatches(value, t))) {
      return [`${path}: 类型应为 ${types.join('|')}，实际为 ${typeOf(value)}`];
    }
  }

  if (schema.const !== undefined && value !== schema.const) {
    errors.push(`${path}: 必须等于 ${JSON.stringify(schema.const)}`);
  }

  if (schema.enum !== undefined && !schema.enum.includes(value)) {
    errors.push(`${path}: 取值 ${JSON.stringify(value)} 不在枚举 [${schema.enum.join(', ')}] 中`);
  }

  if (typeof value === 'string') {
    if (schema.minLength !== undefined && value.length < schema.minLength) {
      errors.push(`${path}: 长度 ${value.length} 小于下限 ${schema.minLength}`);
    }
    if (schema.maxLength !== undefined && value.length > schema.maxLength) {
      errors.push(`${path}: 长度 ${value.length} 超过上限 ${schema.maxLength}`);
    }
    if (schema.pattern !== undefined && !new RegExp(schema.pattern, 'u').test(value)) {
      errors.push(`${path}: 不符合格式 ${schema.pattern}`);
    }
  }

  if (typeof value === 'number') {
    if (schema.minimum !== undefined && value < schema.minimum) {
      errors.push(`${path}: ${value} 小于最小值 ${schema.minimum}`);
    }
    if (schema.maximum !== undefined && value > schema.maximum) {
      errors.push(`${path}: ${value} 大于最大值 ${schema.maximum}`);
    }
    if (schema.exclusiveMinimum !== undefined && value <= schema.exclusiveMinimum) {
      errors.push(`${path}: ${value} 必须大于 ${schema.exclusiveMinimum}`);
    }
    if (schema.exclusiveMaximum !== undefined && value >= schema.exclusiveMaximum) {
      errors.push(`${path}: ${value} 必须小于 ${schema.exclusiveMaximum}`);
    }
  }

  if (Array.isArray(value)) {
    if (schema.minItems !== undefined && value.length < schema.minItems) {
      errors.push(`${path}: 元素数 ${value.length} 少于 ${schema.minItems}`);
    }
    if (schema.maxItems !== undefined && value.length > schema.maxItems) {
      errors.push(`${path}: 元素数 ${value.length} 超过 ${schema.maxItems}`);
    }
    if (schema.uniqueItems === true) {
      const seen = new Set();
      value.forEach((v, i) => {
        const k = JSON.stringify(v);
        if (seen.has(k)) errors.push(`${path}[${i}]: 存在重复元素`);
        seen.add(k);
      });
    }
    if (schema.items !== undefined) {
      value.forEach((v, i) => {
        errors.push(...validate(schema.items, v, root, `${path}[${i}]`));
      });
    }
  }

  if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
    if (Array.isArray(schema.required)) {
      for (const key of schema.required) {
        if (!(key in value)) errors.push(`${path}: 缺少必填字段 "${key}"`);
      }
    }
    const props = schema.properties || {};
    for (const [key, v] of Object.entries(value)) {
      if (props[key] !== undefined) {
        errors.push(...validate(props[key], v, root, `${path}.${key}`));
      } else if (schema.additionalProperties === false) {
        errors.push(`${path}: 出现未声明字段 "${key}"`);
      } else if (typeof schema.additionalProperties === 'object') {
        errors.push(...validate(schema.additionalProperties, v, root, `${path}.${key}`));
      }
    }
  }

  if (Array.isArray(schema.allOf)) {
    for (const sub of schema.allOf) errors.push(...validate(sub, value, root, path));
  }
  if (Array.isArray(schema.anyOf)) {
    const results = schema.anyOf.map((sub) => validate(sub, value, root, path));
    if (!results.some((r) => r.length === 0)) {
      errors.push(`${path}: 不满足 anyOf 中任一分支`);
    }
  }
  if (Array.isArray(schema.oneOf)) {
    const passed = schema.oneOf.filter((sub) => validate(sub, value, root, path).length === 0);
    if (passed.length !== 1) errors.push(`${path}: oneOf 需恰好命中 1 个分支，实际 ${passed.length}`);
  }

  return errors;
}
