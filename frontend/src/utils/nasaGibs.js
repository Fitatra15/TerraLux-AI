/**
 * NASA GIBS (Global Imagery Browse Services) TrueColor Satellite Layer
 * Layer: MODIS_Terra_CorrectedReflectance_TrueColor
 * Resolution: Level 9 (~250m native satellite resolution)
 */
export function getNasaGibsTileUrl() {
  // 3 days ago guarantees 100% processed global composite without cloud latency
  const d = new Date(Date.now() - 3 * 86400000);
  const dateStr = d.toISOString().split('T')[0];
  return `https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/${dateStr}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpeg`;
}

export const NASA_GIBS_ATTRIBUTION = 'Imagery &copy; NASA EOSDIS GIBS';
