// Copyright 2017 PDFium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Original code copyright 2014 Foxit Software Inc. http://www.foxitsoftware.com

#include "fxjs/xfa/cjx_time.h"

#include "xfa/fxfa/parser/cxfa_time.h"

CJX_Time::CJX_Time(CXFA_Time* node) : CJX_Content(node) {}

CJX_Time::~CJX_Time() = default;

void CJX_Time::use(CFXJSE_Value* pValue,
                   bool bSetting,
                   XFA_Attribute eAttribute) {
  ScriptAttributeString(pValue, bSetting, eAttribute);
}

void CJX_Time::defaultValue(CFXJSE_Value* pValue,
                            bool bSetting,
                            XFA_Attribute eAttribute) {
  ScriptSomDefaultValue(pValue, bSetting, eAttribute);
}

void CJX_Time::usehref(CFXJSE_Value* pValue,
                       bool bSetting,
                       XFA_Attribute eAttribute) {
  ScriptAttributeString(pValue, bSetting, eAttribute);
}

void CJX_Time::value(CFXJSE_Value* pValue,
                     bool bSetting,
                     XFA_Attribute eAttribute) {
  ScriptSomDefaultValue(pValue, bSetting, eAttribute);
}
