from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field

class OCRRequest(BaseModel):
    """OCR识别请求模型"""
    image: str = Field(..., description="图片数据（base64编码）")
    png_fix: bool = Field(False, description="是否修复PNG透明背景问题")
    probability: bool = Field(False, description="是否返回概率信息")
    color_filter_colors: Optional[List[str]] = Field(None, description="颜色过滤预设颜色列表")
    color_filter_custom_ranges: Optional[List[List[List[int]]]] = Field(None, description="自定义HSV颜色范围")
    charset_range: Optional[Union[int, str]] = Field(None, description="字符集范围限制")

class OCRResponse(BaseModel):
    """OCR识别响应模型"""
    text: Optional[str] = Field(None, description="识别的文本")
    probability: Optional[Dict[str, Any]] = Field(None, description="概率信息")


class APIResponse(BaseModel):
    """API响应基础模型"""
    success: bool = Field(..., description="请求是否成功")
    message: str = Field("", description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")