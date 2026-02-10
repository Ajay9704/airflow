/*!
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
import { coerce, lte } from "semver";
import { describe, expect, it } from "vitest";

/**
 * Tests for version parsing logic used in NavTabs.tsx
 * Ensures pre-release versions like "3.1.7rc1" are correctly normalized
 */
describe("Version Parsing with semver.coerce()", () => {
  const parseVersion = (version: string): string | null => {
    const coercedVersion = coerce(version);
    return coercedVersion?.version ?? null;
  };

  it("handles standard semantic versions", () => {
    expect(parseVersion("3.1.7")).toBe("3.1.7");
    expect(parseVersion("3.1.6")).toBe("3.1.6");
    expect(parseVersion("3.0.0")).toBe("3.0.0");
  });

  it("handles release candidate versions (e.g., 3.1.7rc1)", () => {
    expect(parseVersion("3.1.7rc1")).toBe("3.1.7");
    expect(parseVersion("3.1.7rc2")).toBe("3.1.7");
    expect(parseVersion("3.2.0rc1")).toBe("3.2.0");
  });

  it("handles development versions", () => {
    expect(parseVersion("3.1.7.dev0")).toBe("3.1.7");
    expect(parseVersion("3.1.7.dev234")).toBe("3.1.7");
  });

  it("handles versions with v prefix", () => {
    expect(parseVersion("v3.1.7")).toBe("3.1.7");
    expect(parseVersion("v3.1.7rc1")).toBe("3.1.7");
  });

  it("returns null for completely invalid versions", () => {
    expect(parseVersion("")).toBe(null);
    expect(parseVersion("invalid")).toBe(null);
    expect(parseVersion("not-a-version")).toBe(null);
  });
});

describe("Version comparison for legacy router navigation", () => {
  const shouldUseLegacyNavigation = (version: string): boolean | undefined => {
    const coercedVersion = coerce(version);
    const airflowCoreVersion = coercedVersion?.version ?? null;

    if (airflowCoreVersion) {
      return lte(airflowCoreVersion, "3.1.6");
    }
    return undefined;
  };

  it("returns true for versions <= 3.1.6", () => {
    expect(shouldUseLegacyNavigation("3.1.6")).toBe(true);
    expect(shouldUseLegacyNavigation("3.1.5")).toBe(true);
    expect(shouldUseLegacyNavigation("3.0.0")).toBe(true);
  });

  it("returns false for versions > 3.1.6", () => {
    expect(shouldUseLegacyNavigation("3.1.7")).toBe(false);
    expect(shouldUseLegacyNavigation("3.1.7rc1")).toBe(false);
    expect(shouldUseLegacyNavigation("3.2.0")).toBe(false);
    expect(shouldUseLegacyNavigation("4.0.0")).toBe(false);
  });

  it("returns undefined for invalid versions", () => {
    expect(shouldUseLegacyNavigation("invalid")).toBe(undefined);
    expect(shouldUseLegacyNavigation("")).toBe(undefined);
  });
});
